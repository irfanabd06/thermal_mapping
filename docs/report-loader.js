// Builds the report page from the Markdown files in docs/sections/.
//
// To add, remove or reorder sections, edit docs/sections/sections.json.
// Inside a section file you can use:
//   [[table: <table-id> | <caption>]]   inserts a table defined in report-tables.js
//   ![Figure N: caption](assets/file.png)   an image on its own line becomes a captioned figure
//   > TODO: ...                         a yellow draft note (not counted in the word limit)

// The section order lives in sections/sections.json ("report" counts towards the word limit;
// "extras" are references and appendices). It is fetched fresh on every visit, so renaming or
// adding a section never breaks the page because of a cached copy of this script.
const SECTIONS_MANIFEST = "sections/sections.json";

// Tolerates the backslash escapes (\[ \] \|) that rich-text editors may add when saving.
const TABLE_SHORTCODE = /^\s*\\?\[\\?\[\s*table\s*:\s*([\w-]+)\s*(?:\\?\|\s*(.*?))?\s*\\?\]\\?\]\s*$/i;

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

function escapeHtml(text) {
  return text.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
}

function splitFrontmatter(source) {
  const match = source.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
  if (!match) return { meta: {}, body: source };
  const meta = {};
  for (const line of match[1].split("\n")) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (kv) meta[kv[1]] = kv[2].replace(/^["']|["']$/g, "");
  }
  return { meta, body: source.slice(match[0].length) };
}

// Replace [[table: ...]] lines with table placeholders before Markdown parsing.
function expandShortcodes(body) {
  return body
    .split("\n")
    .map((line) => {
      const m = line.match(TABLE_SHORTCODE);
      if (!m) return line;
      const caption = escapeHtml(m[2] || "");
      return `\n<div class="report-table" data-table="${m[1]}" data-caption="${caption}"></div>\n`;
    })
    .join("\n");
}

// Post-process rendered HTML: TODO notes, captioned figures, heading ids.
function enhance(container) {
  container.querySelectorAll("blockquote").forEach((quote) => {
    const text = quote.textContent.trim();
    if (!/^TODO\b/i.test(text)) return;
    const alert = document.createElement("sl-alert");
    alert.className = "todo";
    alert.setAttribute("variant", "warning");
    alert.setAttribute("open", "");
    alert.innerHTML = quote.innerHTML.replace(/TODO\s*:?\s*/i, "");
    quote.replaceWith(alert);
  });

  container.querySelectorAll("div.report-table").forEach((placeholder) => {
    const wrapper = document.createElement("table-component");
    wrapper.setAttribute("subtitle", placeholder.dataset.caption || "");
    const target = document.createElement("div");
    target.id = placeholder.dataset.table;
    wrapper.appendChild(target);
    placeholder.replaceWith(wrapper);
  });

  container.querySelectorAll("p > img:only-child").forEach((img) => {
    const p = img.parentElement;
    if (p.textContent.trim() !== "") return;
    const figure = document.createElement("image-component");
    figure.setAttribute("tag", slugify(img.alt || img.src));
    figure.setAttribute("source", img.getAttribute("src"));
    figure.setAttribute("subtitle", img.alt || "");
    p.replaceWith(figure);
  });

  container.querySelectorAll("h2, h3, h4").forEach((h) => {
    if (!h.id) h.id = slugify(h.textContent);
  });
}

async function loadSection(file) {
  const response = await fetch(`sections/${file}`, { cache: "no-cache" });
  if (!response.ok) throw new Error(`Could not load sections/${file} (${response.status})`);
  const { meta, body } = splitFrontmatter(await response.text());
  const title = meta.title || file.replace(/\.md$/, "");

  const section = document.createElement("div");
  section.className = "report-section";
  section.id = slugify(title);
  section.innerHTML = `<h2>${escapeHtml(title)}</h2>` + marked.parse(expandShortcodes(body));
  enhance(section);
  return section;
}

function buildTableOfContents(roots) {
  const tree = document.getElementById("toc-tree");
  tree.innerHTML = "";
  for (const root of roots) {
    root.querySelectorAll(".report-section").forEach((section) => {
      const top = document.createElement("sl-tree-item");
      const subsections = section.querySelectorAll("h3");
      if (subsections.length) top.setAttribute("expanded", "");
      top.innerHTML = `<a href="#${section.id}">${escapeHtml(section.querySelector("h2").textContent)}</a>`;
      subsections.forEach((h) => {
        const item = document.createElement("sl-tree-item");
        item.innerHTML = `<a href="#${h.id}">${escapeHtml(h.textContent)}</a>`;
        top.appendChild(item);
      });
      tree.appendChild(top);
    });
  }
}

async function buildReport() {
  const body = document.getElementById("report-body");
  const extras = document.getElementById("report-extras");
  try {
    const manifestResponse = await fetch(SECTIONS_MANIFEST, { cache: "no-cache" });
    if (!manifestResponse.ok) throw new Error(`Could not load ${SECTIONS_MANIFEST} (${manifestResponse.status})`);
    const manifest = await manifestResponse.json();
    const main = await Promise.all(manifest.report.map(loadSection));
    const end = await Promise.all((manifest.extras || []).map(loadSection));
    body.replaceChildren();
    main.forEach((section, i) => {
      if (i > 0) body.appendChild(document.createElement("sl-divider"));
      body.appendChild(section);
    });
    extras.replaceChildren();
    end.forEach((section) => {
      extras.appendChild(document.createElement("sl-divider"));
      extras.appendChild(section);
    });
    buildTableOfContents([body, extras]);
    if (typeof renderReportTables === "function") renderReportTables();
    if (location.hash) document.querySelector(location.hash)?.scrollIntoView();
  } catch (error) {
    body.innerHTML = `<p><strong>The report could not be loaded.</strong> ${escapeHtml(String(error))}</p>
      <p>If you opened index.html straight from your computer, run <code>python3 -m http.server</code>
      inside the docs folder and open <code>http://localhost:8000</code> instead.</p>`;
  }
}

buildReport();
