/**
 * Analytics Dashboard
 */

'use strict';
(function () {
  let cardColor, headingColor, labelColor, legendColor, borderColor, shadeColor;

  if (isDarkStyle) {
    cardColor = config.colors_dark.cardColor;
    headingColor = config.colors_dark.headingColor;
    labelColor = config.colors_dark.textMuted;
    legendColor = config.colors_dark.bodyColor;
    borderColor = config.colors_dark.borderColor;
    shadeColor = 'dark';
  } else {
    cardColor = config.colors.cardColor;
    headingColor = config.colors.headingColor;
    labelColor = config.colors.textMuted;
    legendColor = config.colors.bodyColor;
    borderColor = config.colors.borderColor;
    shadeColor = 'light';
  }

  Apex.chart = {
		fontFamily: 'inherit',
		locales: [{
			"name": "fa",
			"options": {
				"months": ["ژانویه", "فوریه", "مارس", "آوریل", "می", "ژوئن", "جولای", "آگوست", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"],
				"shortMonths": ["ژانویه", "فوریه", "مارس", "آوریل", "می", "ژوئن", "جولای", "آگوست", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"],
				"days": ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه"],
				"shortDays": ["ی", "د", "س", "چ", "پ", "ج", "ش"],
				"toolbar": {
					"exportToSVG": "دریافت SVG",
					"exportToPNG": "دریافت PNG",
					"menu": "فهرست",
					"selection": "انتخاب",
					"selectionZoom": "بزرگنمایی قسمت انتخاب شده",
					"zoomIn": "بزرگ نمایی",
					"zoomOut": "کوچک نمایی",
					"pan": "جا به جایی",
					"reset": "بازنشانی بزرگ نمایی"
				}
			}
		}],
		defaultLocale: "fa"
	}

    const EXIT_ANIMATION_DELAY = 400;

    const calculateNonZeroAverage = (series) => {
        if (!Array.isArray(series) || series.length === 0) {
            return 0;
        }

        let sum = 0;
        let count = 0;

        series.forEach(value => {
            if (typeof value === 'number' && value !== 0) {
                sum += value;
                count += 1;
            }
        });

        if (count === 0) {
            return 0;
        }

        return Math.round(sum / count);
    };

    // (Annual Chart)
    const annualExpenseChartEl = document.querySelector('#annualExpenseChart');

    if (annualExpenseChartEl) {
        const yearKindSelect = document.getElementById('yearkind');
        let annualChartInstance = null;

        const averageEl = document.getElementById('annualAverageValue');

        const parseChartData = (rawStr) => {
            if (typeof rawStr !== 'string' || !rawStr.trim()) {
                return [];
            }
            let cleanStr = rawStr.trim();
            cleanStr = cleanStr.replace(/^[\s\uFEFF\u00A0]+|[\s\uFEFF\u00A0]+$/g, '');
            cleanStr = cleanStr.replace(/\s/g, '');
            if (!cleanStr) return [];

            try {
                return JSON.parse(cleanStr);
            } catch (e) {
                console.error("Failed to parse JSON string:", cleanStr, e);
                return [];
            }
        }

        const getChartConfig = (labels, series, kind = 'E') => {

            let color = config.colors.danger;
            let name = 'هزینه';

            if (kind === 'I') {
                color = config.colors.success;
                name = 'درآمد';
            } else if (kind === 'T') {
                color = config.colors.info;
                name = 'انتقال';
            }

            return {
                chart: {
                    height: 275,
                    type: 'bar',
                    toolbar: { show: true },

                    animations: {
                        enabled: true,
                        easing: 'easeinout',
                        speed: 700,
                        animateGradually: {
                            enabled: false,
                        },
                        dynamicAnimation: {
                            enabled: true,
                            speed: 400
                        }
                    },
                    updateSeries: true,
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: '55%',
                        borderRadius: 5,
                        startingShape: 'rounded'
                    },
                },
                dataLabels: { enabled: false },
                colors: [color],
                series: [{
                    name: name,
                    data: series
                }],
                grid: {
                    borderColor: borderColor,
                    padding: { bottom: 0 , left: 50,}
                },
                xaxis: {
                    categories: labels,
                    axisBorder: { show: false },
                    axisTicks: { show: false },
                    labels: {
                        style: { colors: labelColor }
                    },
                },
                yaxis: {
                    title: {
                        style: { colors: labelColor }
                    },
                    labels: {
                        style: { colors: labelColor },
                        minWidth: 50,
                        formatter: function (val) {
                            return val.toLocaleString('fa-IR');
                        }
                    },
                },
                legend: { show: false },
                tooltip: {
                    y: {
                        formatter: function (val) {
                            return val.toLocaleString('fa-IR') + " ریال"
                        }
                    }
                }
            };
        };

        const fetchAndUpdateAnnualChart = (kind) => {
            if (typeof annualChartInstance === 'undefined' || annualChartInstance === null) return;

            const chartDataUrl = annualExpenseChartEl.getAttribute('data-ajax-url') || '/api/annual-data/';
            const url = `${chartDataUrl}?kind=${kind}`;

            let newColor = config.colors.danger;
            let newName = 'هزینه';
            if (kind === 'I') {
                newColor = config.colors.success;
                newName = 'درآمد';
            } else if (kind === 'T') {
                newColor = config.colors.info;
                newName = 'انتقال';
            }

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const average = calculateNonZeroAverage(data.series);
                    const formattedAverage = average.toLocaleString('fa-IR');

                    const fullText = `میانگین ماهانه: ${formattedAverage} ریال`;

                    if (averageEl) {
                        averageEl.textContent = fullText;
                    } else {
                        console.warn("Element with ID 'annualAverageValue' not found.");
                    }

                    const currentDataLength = annualChartInstance.w.config.xaxis.categories.length;

                    const emptySeries = Array(currentDataLength).fill(0);

                    annualChartInstance.updateOptions({
                        series: [{
                            name: annualChartInstance.w.config.series[0].name,
                            data: emptySeries
                        }]
                    }, false, true);

                    setTimeout(() => {
                        annualChartInstance.updateOptions({
                            colors: [newColor],
                            series: [{
                                name: newName,
                                data: data.series
                            }]
                        }, false, true);

                    }, EXIT_ANIMATION_DELAY);
                })
                .catch(error => {
                    console.error('Error fetching annual chart data:', error);
                });
        }

        if (typeof ApexCharts !== 'undefined') {
            const rawLabels = annualExpenseChartEl.getAttribute('data-labels');
            const rawSeries = annualExpenseChartEl.getAttribute('data-series');

            const chartLabels = parseChartData(rawLabels);
            const chartSeries = parseChartData(rawSeries);

            try {
                 if (chartLabels.length > 0 && chartSeries.length > 0) {
                    const initialAverage = calculateNonZeroAverage(chartSeries);
                    const formattedInitialAverage = initialAverage.toLocaleString('fa-IR');
                    const initialFullText = `میانگین ماهانه: ${formattedInitialAverage} ریال`;

                    if (averageEl) {
                        averageEl.textContent = initialFullText;
                    }
                    const initialConfig = getChartConfig(chartLabels, chartSeries, 'E');
                    annualChartInstance = new ApexCharts(annualExpenseChartEl, initialConfig);
                    annualChartInstance.render();
                } else {
                    console.log("Initial annual chart data is empty. Skipping render.");
                }
            } catch (error) {
                console.error("Critical Error: Failed to render initial chart. Original error:", error);
            }
        } else {
            console.error("ApexCharts library is not loaded.");
        }

        if (yearKindSelect) {
            yearKindSelect.addEventListener('change', function() {
                const selectedKind = this.value;
                fetchAndUpdateAnnualChart(selectedKind);
            });
        }
    }

    const monthlyReportCardEl = document.querySelector('#monthlyReportCard');

    if (monthlyReportCardEl) {
        const monthKindSelect = document.getElementById('monthkind');
        const monthlyTotalEl = document.getElementById('monthlyTotalValue');
        const averageDayEl = document.getElementById('averageDay');
        const categoryListEl = document.getElementById('monthlyCategoryList');

        const getProgressBarColor = (category, kind) => {
            switch (kind) {
                case 'E':
                    return 'bg-danger';
                case 'I':
                    return 'bg-success';
                case 'T':
                    return 'bg-info';
                default:
                    return 'bg-secondary';
            }
        }

        const generateCategoryHtml = (categories, currentKind) => {
            let html = '<ul class="p-0 m-0">';

            if (Object.keys(categories).length === 0) {
                html += `<div class="card-body pb-5 d-flex flex-column justify-content-center align-items-center" style="margin-top: 96px">
                    <h6>هنوز هیچ تراکنشی ثبت نشده است.</h6>
                    <p class="text-muted">برای اضافه کردن تراکنش، <a href="{% url 'transactions' %}">اینجا</a> کلیک کنید</p>
                  </div>`;
            } else {
                for (const [categoryName, dataList] of Object.entries(categories)) {
                    const amount = dataList[0];
                    const percent = dataList[1];
                    const categoryId = dataList[2];

                    const percentageValue = parseFloat(percent) || 0;
                    const progressBarColor = getProgressBarColor(categoryName, currentKind);

                    html += `
                    <li class="d-flex align-items-center mb-4 pb-2 px-4">
                      <div class="d-flex flex-column w-100">
                        <div class="d-flex justify-content-between mb-2">
                          <span>
                              ${categoryName}
                              <a href="#" class="tag-detail-link badge bg-label-info ms-2"
                                 data-category-id="${categoryId}"
                                 data-category-kind="${currentKind}"
                                 data-bs-toggle="modal"
                                 data-bs-target="#tagReportModal">
                                  جزئیات تگ‌ها
                              </a>
                          </span>
                          <span class="text-muted">${amount} ریال</span>
                          <span class="text-muted">${percent}٪</span>
                        </div>
                        <div class="progress" style="height: 6px">
                          <div class="progress-bar ${progressBarColor}" style="width: ${percentageValue}%" role="progressbar" aria-valuenow="${percentageValue}" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                      </div>
                    </li>
                    `;
                }
            }

            html += '</ul>';
            return html;
        }

        const fetchAndUpdateMonthlyReport = (kind) => {
            const reportDataUrl = monthlyReportCardEl.getAttribute('data-ajax-url');
            const url = `${reportDataUrl}?kind=${kind}`;

            // نمایش لودینگ
            if (monthlyTotalEl) monthlyTotalEl.innerHTML = '<h3>...</h3>';
            if (averageDayEl) averageDayEl.textContent = '...';
            if (categoryListEl) categoryListEl.innerHTML = '<p class="text-center py-5">در حال بارگذاری...</p>';


            fetch(url)
                .then(response => {
                     if (!response.ok) {
                         throw new Error(`HTTP error! status: ${response.status}`);
                     }
                     return response.json();
                })
                .then(data => {
                    try {
                        if (monthlyTotalEl) {
                            monthlyTotalEl.innerHTML = `${data.total_amount} <small class="text-muted fs-5">ریال</small>`;
                        }

                        if (averageDayEl) {
                            averageDayEl.textContent = `میانگین روزانه: ${data.average_daily} ریال`;
                        }

                        if (categoryListEl) {
                            categoryListEl.innerHTML = generateCategoryHtml(data.categories_summary, kind);
                        }
                    } catch (e) {
                        console.error('JS Rendering Error inside fetch().then():', e);
                        if (monthlyTotalEl) monthlyTotalEl.innerHTML = '<h3>خطای رندر JS</h3>';
                        if (categoryListEl) categoryListEl.innerHTML = '<p class="text-center py-5 text-danger">خطای پردازش داده‌ها! کنسول را بررسی کنید.</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching monthly report data (Server/Network):', error);
                    if (monthlyTotalEl) monthlyTotalEl.innerHTML = '<h3>خطا در سرور/شبکه</h3>';
                });
        }

        const initialRenderAverageDay = () => {
            try {
                const initialTotalRaw = parseFloat(monthlyReportCardEl.getAttribute('data-initial-total')) || 0;
                const daysPassed = parseInt(monthlyReportCardEl.getAttribute('data-days-passed')) || 1;

                let averageDaily = 0;

                if (daysPassed > 0 && initialTotalRaw > 0) {
                    averageDaily = Math.round(initialTotalRaw / daysPassed);
                }

                const formattedAverage = averageDaily.toLocaleString('fa-IR');

                if (averageDayEl) {
                    averageDayEl.textContent = `میانگین روزانه: ${formattedAverage} ریال`;
                }
            } catch (e) {
                console.error("Error in initialRenderAverageDay:", e);
            }
        }

        initialRenderAverageDay();

        if (monthKindSelect) {
            monthKindSelect.addEventListener('change', function() {
                const selectedKind = this.value;
                fetchAndUpdateMonthlyReport(selectedKind);
            });
        }
    }
})();