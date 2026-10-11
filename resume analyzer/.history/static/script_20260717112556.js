const form = document.getElementById("analyzeForm");
const fileInput = document.getElementById("resumeFile");
const fileDrop = document.getElementById("fileDrop");
const fileLabel = document.getElementById("fileLabel");
const jobDescription = document.getElementById("jobDescription");
const jdWordCount = document.getElementById("jdWordCount");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const errorBox = document.getElementById("errorBox");
const results = document.getElementById("results");

// ---------- File picker / drag & drop ----------
fileDrop.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
    fileLabel.textContent = `📎 ${fileInput.files[0].name}`;
    fileDrop.classList.add("has-file");
  }
});

["dragover", "dragenter"].forEach(evt => {
  fileDrop.addEventListener(evt, (e) => {
    e.preventDefault();
    fileDrop.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach(evt => {
  fileDrop.addEventListener(evt, (e) => {
    e.preventDefault();
    fileDrop.classList.remove("dragover");
  });
});

fileDrop.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    fileLabel.textContent = `📎 ${file.name}`;
    fileDrop.classList.add("has-file");
  }
});

// ---------- Word count for JD ----------
jobDescription.addEventListener("input", () => {
  const words = jobDescription.value.trim();
  jdWordCount.textContent = `${words ? words.split(/\s+/).length : 0} words`;
});

// ---------- Clear ----------
clearBtn.addEventListener("click", () => {
  form.reset();
  fileLabel.textContent = "Click to choose a file, or drag one here";
  fileDrop.classList.remove("has-file");
  jdWordCount.textContent = "0 words";
  results.classList.add("hidden");
  hideError();
});

function hideError() {
  errorBox.classList.add("hidden");
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function renderTags(containerId, skills, cssClass) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  if (!skills || skills.length === 0) {
    container.innerHTML = '<span class="empty-note">None found</span>';
    return;
  }

  skills.forEach(skill => {
    const tag = document.createElement("span");
    tag.className = `tag ${cssClass}`;
    tag.textContent = skill;
    container.appendChild(tag);
  });
}

// ---------- Submit ----------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();

  if (!fileInput.files.length) {
    showError("Please upload a resume file.");
    return;
  }
  if (!jobDescription.value.trim()) {
    showError("Please paste a job description.");
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  results.classList.add("hidden");

  const formData = new FormData();
  formData.append("resume_file", fileInput.files[0]);
  formData.append("job_description", jobDescription.value);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    document.getElementById("finalScore").textContent = `${data.final_score}%`;
    document.getElementById("similarityScore").textContent = `${data.similarity_score}%`;
    document.getElementById("skillCoverage").textContent = `${data.skill_coverage}%`;

    document.getElementById("matchedCount").textContent = data.matched_skills.length;
    document.getElementById("missingCount").textContent = data.missing_skills.length;

    renderTags("matchedSkills", data.matched_skills, "matched");
    renderTags("missingSkills", data.missing_skills, "missing");
    renderTags("extraSkills", data.extra_skills, "");

    results.classList.remove("hidden");
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    showError("Could not reach the server. Please check the app is running.");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Match";
  }
});