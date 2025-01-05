
        const finance_view = data.finance_view
        const category_wise_data = data.category_wise_data
        const savings = data.savings
        const year_wise_data = data.year_wise_data
        const category_wise_month = data.category_wise_month
        
        // Data placeholders (replace with your dynamic data as needed)
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
        // Financial Overview Progress Bar Chart (Income, Expense, Savings, Investment)
        new Chart(document.getElementById("financialOverviewChart").getContext("2d"), {
            type: "bar",
            data: {
                labels: finance_view.labels,
                datasets: [{
                    label: "Finance",
                    data: finance_view.data, // Example values
                    // backgroundColor:finance_view.labels.map(() => getRandomColor()) ,
                    backgroundColor:["#4a90e2","#7bbf7e","#b86b4b","#555555","#f1e0c6 "] ,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,   
                indexAxis: "y",  // Horizontal bars
                plugins: {
                    title: {
                        display: true,
                        text: "Financial Overview"
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: finance_view.max,  // Adjust based on your data range
                        title: {
                            display: true,
                            text: 'Amount (₹)'
                        }
                    }
                }
            }
        });

// Expense by Category Pie Chart
new Chart(document.getElementById("expenseCategoryChart"), {
    type: "pie",
    data: {
        labels: Object.keys(category_wise_data),
        datasets: [{
            label: "Category",
            data: Object.values(category_wise_data),
            backgroundColor: [
                "#f76c5e", 
                "#a1e6c6", 
                "#9b7bbf", 
                "#f1c40f", 
                "#1abc9c", 
                "#e67e22", 
                "#7f8c8d", 
                "#d1b2a1", 
                "#f5a623", 
                "#8e8b3b"
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: "Category-wise Expense Distribution"
            },
            legend: {
                position: 'top',
            }
        }
    }
});

    
        // Month-wise Savings Chart
    new Chart(document.getElementById("savingsChart"), {
        type: "line",
        data: {
            labels: Object.keys(savings).reverse(),
            datasets: [{
                label: "Savings (₹)",
                data: Object.values(savings).reverse(),
                borderColor: "var(--primary)",
                backgroundColor: "rgba(176, 163, 111, 0.2)" ,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Month-wise Savings"
                }
            }
        }
    });

        // Sub Chart 1: Year-wise Income and Expense
        new Chart(document.getElementById("subChart1").getContext("2d"), {
            type: "bar",
            data: {
                labels: year_wise_data.label,
                datasets: [
                    {
                        label: "Income (₹)",
                        data:  year_wise_data.income,
                        backgroundColor: "#4a90e2"
                    },
                    {
                        label: "Expense (₹)",
                        data:  year_wise_data.expense,
                        backgroundColor: "#7bbf7e"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: "Year-wise Income and Expense"
                    }
                }
            }
        });

        // Sub Chart 2: Current Month Expense as Percentage of Total Income
        new Chart(document.getElementById("subChart2").getContext("2d"), {
            type: "doughnut",
            data: {
                labels: category_wise_month.labels,
                datasets: [{
                    data: category_wise_month.amount,
                    backgroundColor:[
                        "#f76c5e", 
                        "#a1e6c6", 
                        "#9b7bbf", 
                        "#f1c40f", 
                        "#1abc9c", 
                        "#e67e22", 
                        "#7f8c8d", 
                        "#d1b2a1", 
                        "#f5a623", 
                        "#8e8b3b"  
                      ],
                      
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: "Current Month Expense Out of Total Income"
                    }
                }
            }
        });


    
