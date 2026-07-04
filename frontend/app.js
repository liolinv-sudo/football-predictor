async function loadMatches() {

    const res = await fetch("/matches");
    let matches = await res.json();

    // 🔝 sortera EV
    matches.sort((a, b) => b.ev - a.ev);

    const body = document.getElementById("body");
    body.innerHTML = "";

    matches.forEach(m => {

        const tr = document.createElement("tr");

        // 🟢 / 🔴 färg
        if (m.ev > 0) {
            tr.classList.add("row-green");
        } else {
            tr.classList.add("row-red");
        }

        tr.innerHTML = `
            <td>${m.home} - ${m.away}</td>
            <td>${m.ev.toFixed(3)}</td>
            <td>${(m.kelly * 100).toFixed(1)}%</td>
            <td>${JSON.stringify(m.odds)}</td>
        `;

        body.appendChild(tr);
    });
}

loadMatches();
