const form = document.querySelector("#shorten-form");
const input = document.querySelector("#long-url");
const message = document.querySelector("#message");
const result = document.querySelector("#result");
const shortUrlLink = document.querySelector("#short-url");
const copyButton = document.querySelector("#copy-button");

let latestShortUrl = "";

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "Creating short URL...";
  message.className = "message";
  result.hidden = true;

  try {
    const response = await fetch("/api/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ long_url: input.value }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    latestShortUrl = data.short_url;
    shortUrlLink.href = latestShortUrl;
    shortUrlLink.textContent = latestShortUrl;
    result.hidden = false;
    message.textContent = "Short URL created.";
    message.classList.add("success");
  } catch (error) {
    message.textContent = error.message;
    message.classList.add("error");
  }
});

copyButton.addEventListener("click", async () => {
  if (!latestShortUrl) return;

  await navigator.clipboard.writeText(latestShortUrl);
  copyButton.textContent = "Copied";

  window.setTimeout(() => {
    copyButton.textContent = "Copy";
  }, 1200);
});
