document.getElementById("submit").addEventListener("click", async () => {
  const id = document.getElementById("student-id").value.trim();
  const messageEl = document.getElementById("message");
  const schedule = document.getElementById("schedule");

  messageEl.textContent = "";
  schedule.innerHTML = "";
  document.getElementById("student-info").innerHTML = "";

  if (!id) {
    messageEl.textContent = "الرجاء إدخال رقم المتدرب";
    return;
  }

  try {
    const res  = await fetch(`/api/schedule/${id}`);
    const data = await res.json();

    if (data.success) {
      document.getElementById("student-info").innerHTML =
        `<h2>${data.name}</h2><p>${data.major}</p>`;
      schedule.innerHTML = data.scheduleHtml;
    } else {
      messageEl.textContent = data.message || "لا توجد بيانات.";
    }
  } catch (err) {
    messageEl.textContent = "تعذّر الاتصال بالخادم.";
  }
});

