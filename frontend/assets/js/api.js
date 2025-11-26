async function apiGet(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("GET " + url + " failed");
  return res.json();
}

async function apiPost(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("POST " + url + " failed");
  return res.json();
}

/*--------------------------------------------------
  FIXED loadShell() — working in Windows, VS Code,
  Live Server, Python server, Flask, etc.
--------------------------------------------------*/
async function loadShell() {
  const navHolder = document.getElementById("navbar");
  const footHolder = document.getElementById("footer");

  // Use RELATIVE PATHS instead of "/components/..."
  // Because absolute paths break on Windows file:// URLs

  if (navHolder) {
    try {
      const navResp = await fetch("components/navbar.html");
      navHolder.innerHTML = await navResp.text();
    } catch (e) {
      console.error("Navbar load failed:", e);
    }
  }

  if (footHolder) {
    try {
      const footResp = await fetch("components/footer.html");
      footHolder.innerHTML = await footResp.text();
    } catch (e) {
      console.error("Footer load failed:", e);
    }
  }
}
