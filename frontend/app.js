async function loadMatches() {

    const response = await fetch(
        "https://DIN-APP.onrender.com/matches"
    );

    const matches = await response.json();

    const container =
        document.getElementById("matches");

    matches.sort((a, b) => b.ev - a.ev);

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

let evColor = match.ev > 0 ? "green" : "red";
div.innerHTML = `
    <h3>${match.home} - ${match.away}</h3>

    <p style="color:${evColor}">
        EV: ${match.ev}
    </p>
`;

<p>Kelly: ${(match.kelly * 100).toFixed(1)}%</p>

if (match.arbitrage) {
    div.innerHTML += `
        <p style="color:blue;">
            🟢 Arbitrage: ${(match.arb_percent * 100).toFixed(2)}%
        </p>
    `;
}
