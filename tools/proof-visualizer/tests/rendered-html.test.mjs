import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const developmentPreviewMeta =
  /<meta(?=[^>]*\bname=["']codex-preview["'])(?=[^>]*\bcontent=["']development["'])[^>]*>/i;

async function render(pathname = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${pathname}`, {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the proof bonsai shell and scientific boundary", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Proof Bonsai · Krenn–Gu research map<\/title>/i);
  assert.match(html, /Proof Bonsai/);
  assert.match(html, /UNRESOLVED/);
  assert.match(html, /Exact repository status/);
  assert.match(html, /Established at the node/);
  assert.match(html, /open, partial, conditional, or unresolved boundary/);
  assert.match(html, /refuted or retired/);
  assert.match(html, /Nearby/);
  assert.match(html, /Whole map/);
  assert.match(html, /one-edge neighborhood/);
  assert.match(html, /Copy node link/);
  assert.match(html, /Source topology aligned/);
  assert.doesNotMatch(html, developmentPreviewMeta);
  assert.doesNotMatch(html, /Your site is taking shape|react-loading-skeleton/);
});
test("server-renders the append-only public field notes boundary", async () => {
  const response = await render("/field-notes");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>Field Notes · Proof Bonsai<\/title>/i);
  assert.match(html, /Agent report, not evidence/);
  assert.match(html, /UNRESOLVED/);
  assert.match(html, /old notes are never rewritten/i);
  assert.match(html, /GLD101/);
  assert.doesNotMatch(html, /progress percentage|solved fraction|confidence meter/i);
});
test("removes starter-only preview infrastructure", async () => {
  const [page, layout, packageJson] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
    readFile(new URL("../package.json", import.meta.url), "utf8"),
  ]);

  assert.match(page, /<ProofBonsai/);
  assert.match(layout, /Proof Bonsai/);
  assert.doesNotMatch(page, /_sites-preview|SkeletonPreview|codex-preview/);
  assert.doesNotMatch(layout, /Starter Project|codex-preview/);
  assert.doesNotMatch(packageJson, /react-loading-skeleton/);
  await assert.rejects(access(new URL("../app/_sites-preview", import.meta.url)));
});
