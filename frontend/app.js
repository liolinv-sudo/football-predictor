async function loadMatches() {

    const response = await fetch(
        "https://DIN-APP.onrender.com/matches"
    );

    const matches = await response.json();

    const container =
        document.getElementById("matches");

    matches.forEach(match => {

        const div =
            document.createElement("div");

        div.className = "match";

        div.innerHTML = `
            <h3>${match.home} - ${match.away}</h3>

            <p>EV: ${match.ev}</p>

            <p>
                Odds:
                ${JSON.stringify(match.odds)}
            </p>
        `;

        container.appendChild(div);
    });
}

loadMatches();
