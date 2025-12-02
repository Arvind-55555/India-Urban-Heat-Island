// ============================================
// Urban Heat Island Dashboard - JavaScript
// ============================================

// Smooth Scrolling for Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Update active link
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        // Smooth scroll to section
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Intersection Observer for Scroll Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.overview-card, .viz-card, .insight-card, .recommendation-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s, transform 0.6s';
    observer.observe(card);
});

// Chart.js Interactive Visualizations
document.addEventListener('DOMContentLoaded', function() {
    // Chart 1: UHI Intensity Distribution
    const uhiDistCtx = document.getElementById('uhiDistribution');
    if (uhiDistCtx) {
        new Chart(uhiDistCtx, {
            type: 'bar',
            data: {
                labels: ['0-1°C', '1-2°C', '2-3°C', '3-4°C', '>4°C'],
                datasets: [{
                    label: 'Number of Cities',
                    data: [5, 19, 16, 10, 0],
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(220, 38, 38, 0.8)'
                    ],
                    borderColor: [
                        'rgb(16, 185, 129)',
                        'rgb(59, 130, 246)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)',
                        'rgb(220, 38, 38)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'UHI Intensity Distribution Across Cities',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Cities'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'UHI Intensity Range'
                        }
                    }
                }
            }
        });
    }

    // Chart 2: Regional Comparison
    const regionalCtx = document.getElementById('regionalComparison');
    if (regionalCtx) {
        new Chart(regionalCtx, {
            type: 'doughnut',
            data: {
                labels: ['North (>28°N)', 'North-Central (23-28°N)', 'Central (15-23°N)', 'South (<15°N)'],
                datasets: [{
                    label: 'Average UHI Intensity',
                    data: [2.87, 2.29, 2.44, 1.49],
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)'
                    ],
                    borderColor: [
                        'rgb(239, 68, 68)',
                        'rgb(245, 158, 11)',
                        'rgb(59, 130, 246)',
                        'rgb(16, 185, 129)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Regional UHI Intensity Comparison',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '°C';
                            }
                        }
                    }
                }
            }
        });
    }

    // Chart 3: Land Cover Analysis
    const landCoverCtx = document.getElementById('landCoverAnalysis');
    if (landCoverCtx) {
        new Chart(landCoverCtx, {
            type: 'bar',
            data: {
                labels: ['Industrial', 'Urban', 'Mixed Urban', 'Green Space'],
                datasets: [{
                    label: 'Avg UHI Intensity (°C)',
                    data: [3.31, 2.98, 2.12, 0.91],
                    backgroundColor: 'rgba(239, 68, 68, 0.8)',
                    borderColor: 'rgb(239, 68, 68)',
                    borderWidth: 2,
                    yAxisID: 'y'
                }, {
                    label: 'Avg NDVI',
                    data: [0.09, 0.09, 0.10, 0.22],
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgb(16, 185, 129)',
                    borderWidth: 2,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Land Cover Type vs UHI & Vegetation',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'UHI Intensity (°C)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'NDVI (0-1)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // Chart 4: Top Contributing Factors
    const topFactorsCtx = document.getElementById('topFactors');
    if (topFactorsCtx) {
        new Chart(topFactorsCtx, {
            type: 'horizontalBar',
            data: {
                labels: [
                    'Impervious Surfaces',
                    'Building Density',
                    'NDVI (Vegetation)',
                    'Albedo',
                    'Urban Greenness',
                    'Wind Speed'
                ],
                datasets: [{
                    label: 'Correlation Coefficient',
                    data: [0.742, 0.704, -0.704, -0.699, -0.657, -0.543],
                    backgroundColor: function(context) {
                        const value = context.parsed.x;
                        return value > 0 ? 'rgba(239, 68, 68, 0.8)' : 'rgba(16, 185, 129, 0.8)';
                    },
                    borderColor: function(context) {
                        const value = context.parsed.x;
                        return value > 0 ? 'rgb(239, 68, 68)' : 'rgb(16, 185, 129)';
                    },
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Top UHI Contributing Factors (Correlation)',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Correlation with UHI Intensity'
                        },
                        min: -1,
                        max: 1
                    }
                }
            }
        });
    }
});

// Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(start);
        }
    }, 16);
}

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const target = parseFloat(stat.textContent);
                if (!isNaN(target)) {
                    animateCounter(stat, target);
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statBoxes = document.querySelectorAll('.stat-insight');
statBoxes.forEach(box => statsObserver.observe(box));

// Highlight active section in navigation
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('.section');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + sectionId) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Print Functionality
function printReport() {
    window.print();
}

// Export Data Functionality
function exportData(format) {
    console.log('Exporting data in ' + format + ' format');
    // Implementation would depend on backend or use libraries like jsPDF
}

// Tooltip Functionality
const tooltipElements = document.querySelectorAll('[data-tooltip]');
tooltipElements.forEach(element => {
    element.addEventListener('mouseenter', function() {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = this.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);
        
        const rect = this.getBoundingClientRect();
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
        tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    });
    
    element.addEventListener('mouseleave', function() {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    });
});

// Console Log Welcome Message
console.log('%c Urban Heat Island Dashboard ', 'background: #667eea; color: white; font-size: 20px; padding: 10px;');
console.log('%c Data for 50 Major Indian Cities | 31 Features | Real-time Analysis ', 'color: #667eea; font-size: 14px;');
console.log('%c Built with ❤️ for climate-resilient urban planning ', 'color: #10b981; font-size: 12px;');

// Page Load Animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Responsive Menu Toggle (for mobile)
const menuToggle = document.createElement('button');
menuToggle.className = 'menu-toggle';
menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
menuToggle.style.display = 'none';

// Insert menu toggle if viewport is small
function checkViewport() {
    if (window.innerWidth <= 768) {
        menuToggle.style.display = 'block';
    } else {
        menuToggle.style.display = 'none';
    }
}

window.addEventListener('resize', checkViewport);
checkViewport();

// Back to Top Button
const backToTopButton = document.createElement('button');
backToTopButton.className = 'back-to-top';
backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopButton.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    cursor: pointer;
    display: none;
    z-index: 1000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
`;

document.body.appendChild(backToTopButton);

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTopButton.style.display = 'flex';
        backToTopButton.style.alignItems = 'center';
        backToTopButton.style.justifyContent = 'center';
    } else {
        backToTopButton.style.display = 'none';
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

backToTopButton.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-5px)';
    this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
});

backToTopButton.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
    this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
});

