document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var searchInput = document.getElementById("searchInput").value.trim();
    var ebayResultsDiv = document.getElementById("ebayResults");
    ebayResultsDiv.innerHTML = ""; // Clear previous eBay results
    if (searchInput !== "") {
        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: searchInput })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok (${response.status} - ${response.statusText})`);
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                ebayResultsDiv.innerHTML = "<p>No eBay results found.</p>";
            } else {
                showResults(data, ebayResultsDiv);
            }
        })
        .catch(error => {
            console.error("Error:", error.message);
            ebayResultsDiv.innerHTML = `<p class='error'>${error.message}</p>`;
        });
    } else {
        ebayResultsDiv.innerHTML = "<p class='error'>Please enter a product name.</p>";
    }
});

function showResults(results, ebayResultsDiv) {
    results.forEach(function(product) {
        var productDiv = document.createElement("div");
        productDiv.innerHTML = `
            <h3>${product.name}</h3>
            <p>Price: ${product.price}</p>
            <p>Retailer: ${product.retailer}</p>
            <a href="${product.link}" target="_blank">Buy Now</a>
        `;
        if (product.retailer === "eBay") {
            ebayResultsDiv.appendChild(productDiv);
        } 
    });
}
