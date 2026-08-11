document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("studentSearch");
  const results = document.getElementById("searchResults");
  if (!input || !results) return;

  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      const q = input.value.trim();
      if (!q) {
        results.innerHTML = "";
        return;
      }
      const response = await fetch(`/api/students?q=${encodeURIComponent(q)}`);
      const students = await response.json();
      results.innerHTML = students.length
        ? `<div class="list-group">${students.map(s =>
            `<a class="list-group-item list-group-item-action" href="/students/${s.id}">
              <strong>${escapeHtml(s.name)}</strong> — ${escapeHtml(s.email)}
            </a>`).join("")}</div>`
        : `<div class="text-muted small">No matching students.</div>`;
    }, 250);
  });
});

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[char]));
}
