import { expect, test } from "@playwright/test";

const provider = {
  id: "provider-1",
  name: "Test OpenAI",
  kind: "openai",
  base_url: "http://localhost:11434/v1",
  api_key: "fake-key",
  model_default: "llama3.2",
};

const workflow = {
  id: "flow-1",
  name: "Test Flow",
  nodes: [],
  edges: [],
};

test.describe("smoke", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/api/v1/providers", async (route, request) => {
      if (request.method() === "GET") {
        await route.fulfill({ json: [provider] });
      } else {
        const body = await request.postDataJSON();
        await route.fulfill({ json: { ...provider, ...body, id: "provider-1" } });
      }
    });

    await page.route("**/api/v1/flows", async (route, request) => {
      const body = await request.postDataJSON();
      await route.fulfill({ json: { ...workflow, ...body, id: "flow-1" } });
    });

    await page.route("**/api/v1/flows/*/run", async (route) => {
      const id = route.request().url().split("/").pop();
      await route.fulfill({
        json: {
          workflow_id: id,
          outputs: {
            "node-1": { status: "success", output: "hello" },
            "node-2": { status: "success", output: "Hello from the model" },
          },
        },
      });
    });

    await page.goto("/");
  });

  test("creates provider, builds flow, runs, and shows result", async ({ page }) => {
    await page.getByPlaceholder("Name").fill("Test OpenAI");
    await page.getByPlaceholder("Base URL").fill("http://localhost:11434/v1");
    await page.getByPlaceholder("Default model").fill("llama3.2");
    await page.getByPlaceholder("API key", { exact: false }).fill("fake-key");
    await page.getByRole("button", { name: /create/i }).click();

    await expect(page.getByText("Test OpenAI")).toBeVisible();
    await page.getByText("Test OpenAI").click();

    await page.getByRole("button", { name: /prompt/i }).click();
    await page.getByRole("button", { name: /llm/i }).click();

    await page.locator(".react-flow__node").first().waitFor();
    await page.locator(".react-flow__node").nth(1).waitFor();

    await page.getByRole("button", { name: /save/i }).click();
    await page.getByRole("button", { name: /run flow/i }).click();

    await expect(page.getByText("Hello from the model")).toBeVisible();
    await page.screenshot({ path: "e2e/screenshots/smoke-success.png" });
  });

  test("shows error when a node run fails", async ({ page }) => {
    await page.route("**/api/v1/flows/*/run", async (route) => {
      const id = route.request().url().split("/").pop();
      await route.fulfill({
        json: {
          workflow_id: id,
          outputs: {
            "node-1": { status: "success", output: "hello" },
            "node-2": { status: "error", error: "Provider not configured" },
          },
        },
      });
    });

    await page.getByPlaceholder("Name").fill("Test OpenAI");
    await page.getByPlaceholder("Base URL").fill("http://localhost:11434/v1");
    await page.getByPlaceholder("Default model").fill("llama3.2");
    await page.getByPlaceholder("API key", { exact: false }).fill("fake-key");
    await page.getByRole("button", { name: /create/i }).click();
    await page.getByText("Test OpenAI").click();

    await page.getByRole("button", { name: /prompt/i }).click();
    await page.getByRole("button", { name: /llm/i }).click();
    await page.getByRole("button", { name: /save/i }).click();
    await page.getByRole("button", { name: /run flow/i }).click();

    await expect(page.getByText("Provider not configured")).toBeVisible();
    await page.screenshot({ path: "e2e/screenshots/smoke-error.png" });
  });
});
