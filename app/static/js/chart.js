
document.addEventListener("DOMContentLoaded", function () {

    // Income vs. Expenses chart
    const chartElement = document.getElementById("chart-data");

    if (chartElement) {
        const chartData = JSON.parse(chartElement.textContent);
        const ctx = document.getElementById("incomeExpenseChart");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Finances"],
                datasets: [
                    {
                        label: "Income",
                        data: [chartData.income],
                        backgroundColor: "#16a34a"
                    },
                    {
                        label: "Expenses",
                        data: [chartData.expenses],
                        backgroundColor: "#dc2626"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Amount (" + chartElement.dataset.currency + ")"
                        }
                    }
                }
            }
        });
    }

    // Spending by Category chart
    const categoryElement = document.getElementById("category-chart-data");

    if (categoryElement) {
        const categoryData = JSON.parse(categoryElement.textContent);
        const categoryCtx = document.getElementById("categoryChart");

        new Chart(categoryCtx, {
            type: "doughnut",
            data: {
                labels: categoryData.labels,
                datasets: [
                    {
                        label: "Expenses",
                        data: categoryData.values,
                        backgroundColor: [
                            "#16a34a",
                            "#2563eb",
                            "#dc2626",
                            "#eab308",
                            "#9333ea",
                            "#0891b2",
                            "#f97316"
                        ],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

});
