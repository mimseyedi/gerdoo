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

  // Report Chart
  // --------------------------------------------------------------------

  // Radial bar chart functions
  function radialBarChart(color, value) {
    const radialBarChartOpt = {
      chart: {
        height: 50,
        width: 50,
        type: 'radialBar'
      },
      plotOptions: {
        radialBar: {
          hollow: {
            size: '25%'
          },
          dataLabels: {
            show: false
          },
          track: {
            background: borderColor
          }
        }
      },
      stroke: {
        lineCap: 'round'
      },
      colors: [color],
      grid: {
        padding: {
          top: -8,
          bottom: -10,
          left: -5,
          right: 0
        }
      },
      series: [value],
      labels: ['پیشرفت']
    };
    return radialBarChartOpt;
  }

  const ReportchartList = document.querySelectorAll('.chart-report');
  if (ReportchartList) {
    ReportchartList.forEach(function (ReportchartEl) {
      const color = config.colors[ReportchartEl.dataset.color],
        series = ReportchartEl.dataset.series;
      const optionsBundle = radialBarChart(color, series);
      const reportChart = new ApexCharts(ReportchartEl, optionsBundle);
      reportChart.render();
    });
  }

  // Analytics - Bar Chart
  // --------------------------------------------------------------------
  const analyticsBarChartEl = document.querySelector('#analyticsBarChart'),
    analyticsBarChartConfig = {
      chart: {
        height: 250,
        type: 'bar',
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '20%',
          borderRadius: 3,
          startingShape: 'rounded'
        }
      },
      dataLabels: {
        enabled: false
      },
      colors: [config.colors.primary, config.colors_label.primary],
      series: [
        {
          name: '1400',
          data: [8, 9, 15, 20, 14, 22, 29, 27, 13]
        },
        {
          name: '1401',
          data: [5, 7, 12, 17, 9, 17, 26, 21, 10]
        }
      ],
      grid: {
        borderColor: borderColor,
        padding: {
          bottom: -8
        }
      },
      xaxis: {
        categories: ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          style: {
            colors: labelColor
          }
        }
      },
      yaxis: {
        min: 0,
        max: 30,
        tickAmount: 3,
        labels: {
          style: {
            colors: labelColor
          }
        }
      },
      legend: {
        show: false
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + ' هزار تومان';
          }
        }
      }
    };
  if (typeof analyticsBarChartEl !== undefined && analyticsBarChartEl !== null) {
    const analyticsBarChart = new ApexCharts(analyticsBarChartEl, analyticsBarChartConfig);
    analyticsBarChart.render();
  }

  // Referral - Line Chart
  // --------------------------------------------------------------------
  const referralLineChartEl = document.querySelector('#referralLineChart'),
    referralLineChartConfig = {
      series: [
        {
          name: 'سری 1',
          data: [0, 150, 25, 100, 15, 149]
        }
      ],
      chart: {
        height: 100,
        parentHeightOffset: 0,
        parentWidthOffset: 0,
        type: 'line',
        toolbar: {
          show: false
        }
      },
      markers: {
        size: 6,
        colors: 'transparent',
        strokeColors: 'transparent',
        strokeWidth: 4,
        discrete: [
          {
            fillColor: cardColor,
            seriesIndex: 0,
            dataPointIndex: 5,
            strokeColor: config.colors.success,
            strokeWidth: 4,
            size: 6,
            radius: 2
          }
        ],
        hover: {
          size: 7
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        width: 4,
        curve: 'smooth'
      },
      grid: {
        show: false,
        padding: {
          top: -25,
          bottom: -20
        }
      },
      colors: [config.colors.success],
      xaxis: {
        show: false,
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          show: false
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      }
    };

  if (typeof referralLineChartEl !== undefined && referralLineChartEl !== null) {
    const referralLineChart = new ApexCharts(referralLineChartEl, referralLineChartConfig);
    referralLineChart.render();
  }

  // Conversion - Bar Chart
  // --------------------------------------------------------------------
  const conversionBarChartEl = document.querySelector('#conversionBarchart'),
    conversionBarChartConfig = {
      chart: {
        height: 100,
        stacked: true,
        type: 'bar',
        toolbar: {
          show: false
        },
        sparkline: {
          enabled: true
        }
      },
      plotOptions: {
        bar: {
          columnWidth: '25%',
          borderRadius: 2,
          startingShape: 'rounded'
        },
        distributed: true
      },
      colors: [config.colors.primary, config.colors.warning],
      series: [
        {
          name: 'مشتریان جدید',
          data: [75, 150, 225, 200, 35, 50, 150, 180, 50, 150, 240, 140, 75, 35, 60, 120]
        },
        {
          name: 'مشتریان قدیمی',
          data: [-100, -55, -40, -120, -70, -40, -60, -50, -70, -30, -60, -40, -50, -70, -40, -50]
        }
      ],
      grid: {
        show: false,
        padding: {
          top: 0,
          bottom: -10
        }
      },
      legend: {
        show: false
      },
      dataLabels: {
        enabled: false
      },
      tooltip: {
        x: {
          show: false
        }
      }
    };

  if (typeof conversionBarChartEl !== undefined && conversionBarChartEl !== null) {
    const conversionBarChart = new ApexCharts(conversionBarChartEl, conversionBarChartConfig);
    conversionBarChart.render();
  }

  // Impression - Donut Chart
  // --------------------------------------------------------------------
  const impressionDonutChartEl = document.querySelector('#impressionDonutChart'),
    impressionDonutChartConfig = {
      chart: {
        height: 185,
        type: 'donut'
      },
      dataLabels: {
        enabled: false
      },
      grid: {
        padding: {
          bottom: -10
        }
      },
      series: [80, 30, 60],
      labels: ['اجتماعی', 'ایمیل', 'جستجو'],
      stroke: {
        width: 0,
        lineCap: 'round'
      },
      colors: [config.colors.primary, config.colors.info, config.colors.warning],
      plotOptions: {
        pie: {
          donut: {
            size: '90%',
            labels: {
              show: true,
              name: {
                fontSize: '0.938rem',
                offsetY: 22
              },
              value: {
                show: true,
                fontSize: '1.625rem',
                fontWeight: '500',
                color: headingColor,
                offsetY: -22,
                formatter: function (val) {
                  return val;
                }
              },
              total: {
                show: true,
                label: 'بازدید',
                color: legendColor,
                formatter: function (w) {
                  return w.globals.seriesTotals.reduce(function (a, b) {
                    return a + b;
                  }, 0);
                }
              }
            }
          }
        }
      },
      legend: {
        show: true,
        position: 'bottom',
        offsetY: 8,
        horizontalAlign: 'center',
        labels: {
          colors: legendColor,
          useSeriesColors: false
        },
        markers: {
          width: 10,
          height: 10,
          offsetX: -3
        }
      }
    };

  if (typeof impressionDonutChartEl !== undefined && impressionDonutChartEl !== null) {
    const impressionDonutChart = new ApexCharts(impressionDonutChartEl, impressionDonutChartConfig);
    impressionDonutChart.render();
  }

  // Conversion - Gradient Line Chart
  // --------------------------------------------------------------------
  const conversationChartEl = document.querySelector('#conversationChart'),
    conversationChartConfig = {
      series: [
        {
          data: [50, 100, 0, 60, 20, 30]
        }
      ],
      chart: {
        height: 40,
        type: 'line',
        zoom: {
          enabled: false
        },
        sparkline: {
          enabled: true
        },
        toolbar: {
          show: false
        }
      },
      dataLabels: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      stroke: {
        curve: 'smooth',
        width: 3
      },
      grid: {
        show: false,
        padding: {
          top: 5,
          left: 10,
          right: 10,
          bottom: 5
        }
      },
      colors: [config.colors.primary],
      fill: {
        type: 'gradient',
        gradient: {
          shade: shadeColor,
          type: 'horizontal',
          gradientToColors: undefined,
          opacityFrom: 0,
          opacityTo: 0.9,
          stops: [0, 30, 70, 100]
        }
      },
      xaxis: {
        labels: {
          show: false
        },
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      }
    };
  if (typeof conversationChartEl !== undefined && conversationChartEl !== null) {
    const conversationChart = new ApexCharts(conversationChartEl, conversationChartConfig);
    conversationChart.render();
  }

  // Income - Gradient Line Chart
  // --------------------------------------------------------------------
  const incomeChartEl = document.querySelector('#incomeChart'),
    incomeChartConfig = {
      series: [
        {
          data: [40, 70, 38, 90, 40, 65]
        }
      ],
      chart: {
        height: 40,
        type: 'line',
        zoom: {
          enabled: false
        },
        sparkline: {
          enabled: true
        },
        toolbar: {
          show: false
        }
      },
      dataLabels: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      stroke: {
        curve: 'smooth',
        width: 3
      },
      grid: {
        show: false,
        padding: {
          top: 10,
          left: 10,
          right: 10,
          bottom: 0
        }
      },
      colors: [config.colors.warning],
      fill: {
        type: 'gradient',
        gradient: {
          shade: shadeColor,
          type: 'horizontal',
          gradientToColors: undefined,
          opacityFrom: 0,
          opacityTo: 0.9,
          stops: [0, 30, 70, 100]
        }
      },
      xaxis: {
        labels: {
          show: false
        },
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      }
    };
  if (typeof incomeChartEl !== undefined && incomeChartEl !== null) {
    const incomeChart = new ApexCharts(incomeChartEl, incomeChartConfig);
    incomeChart.render();
  }

  // Registrations Bar Chart
  // --------------------------------------------------------------------
  const registrationsBarChartEl = document.querySelector('#registrationsBarChart'),
    registrationsBarChartConfig = {
      chart: {
        height: 95,
        width: 155,
        type: 'bar',
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          barHeight: '80%',
          columnWidth: '50%',
          startingShape: 'rounded',
          endingShape: 'rounded',
          borderRadius: 2,
          distributed: true
        }
      },
      grid: {
        show: false,
        padding: {
          top: -20,
          bottom: -20,
          left: 0,
          right: 0
        }
      },
      colors: [
        config.colors_label.warning,
        config.colors_label.warning,
        config.colors_label.warning,
        config.colors_label.warning,
        config.colors.warning,
        config.colors_label.warning,
        config.colors_label.warning
      ],
      dataLabels: {
        enabled: false
      },
      series: [
        {
          name: 'سری 1',
          data: [30, 55, 45, 95, 70, 50, 65]
        }
      ],
      legend: {
        show: false
      },
      xaxis: {
        categories: ['د', 'س', 'چ', 'پ', 'ج', 'ش', 'ی'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          show: false
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      }
    };
  if (typeof registrationsBarChartEl !== undefined && registrationsBarChartEl !== null) {
    const registrationsBarChart = new ApexCharts(registrationsBarChartEl, registrationsBarChartConfig);
    registrationsBarChart.render();
  }

  // Sales Bar Chart
  // --------------------------------------------------------------------
  const salesBarChartEl = document.querySelector('#salesChart'),
    salesBarChartConfig = {
      chart: {
        height: 120,
        parentHeightOffset: 0,
        type: 'bar',
        toolbar: {
          show: false
        }
      },
      plotOptions: {
        bar: {
          barHeight: '100%',
          columnWidth: '25px',
          startingShape: 'rounded',
          endingShape: 'rounded',
          borderRadius: 5,
          distributed: true,
          colors: {
            backgroundBarColors: [
              config.colors_label.primary,
              config.colors_label.primary,
              config.colors_label.primary,
              config.colors_label.primary
            ],
            backgroundBarRadius: 5
          }
        }
      },
      grid: {
        show: false,
        padding: {
          top: -30,
          left: -12,
          bottom: 10
        }
      },
      colors: [config.colors.primary],
      dataLabels: {
        enabled: false
      },
      series: [
        {
          name: 'سری 1',
          data: [60, 35, 25, 75, 15, 42, 85]
        }
      ],
      legend: {
        show: false
      },
      xaxis: {
        categories: ['ی', 'د', 'س', 'چ', 'پ', 'ج', 'ش'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          style: {
            colors: labelColor,
            fontSize: '13px'
          }
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      },
      responsive: [
        {
          breakpoint: 1440,
          options: {
            plotOptions: {
              bar: {
                columnWidth: '30%'
              }
            }
          }
        },
        {
          breakpoint: 1200,
          options: {
            plotOptions: {
              bar: {
                columnWidth: '15%'
              }
            }
          }
        },
        {
          breakpoint: 768,
          options: {
            plotOptions: {
              bar: {
                columnWidth: '12%'
              }
            }
          }
        },
        {
          breakpoint: 450,
          options: {
            plotOptions: {
              bar: {
                columnWidth: '19%'
              }
            }
          }
        }
      ]
    };
  if (typeof salesBarChartEl !== undefined && salesBarChartEl !== null) {
    const salesBarChart = new ApexCharts(salesBarChartEl, salesBarChartConfig);
    salesBarChart.render();
  }

  // Growth - Radial Bar Chart
  // --------------------------------------------------------------------
  const growthRadialChartEl = document.querySelector('#growthRadialChart'),
    growthRadialChartConfig = {
      chart: {
        height: 265,
        type: 'radialBar',
        sparkline: {
          show: true
        }
      },
      grid: {
        show: false,
        padding: {
          top: -23,
          bottom: -2
        }
      },
      plotOptions: {
        radialBar: {
          size: 100,
          startAngle: -135,
          endAngle: 135,
          offsetY: 10,
          hollow: {
            size: '55%'
          },
          track: {
            strokeWidth: '50%',
            background: cardColor
          },
          dataLabels: {
            value: {
              offsetY: -22,
              color: headingColor,
              fontWeight: 500,
              fontSize: '26px'
            },
            name: {
              fontSize: '15px',
              color: legendColor,
              offsetY: 20
            }
          }
        }
      },
      colors: [config.colors.danger],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'horizontal',
          shadeIntensity: 0.5,
          gradientToColors: [config.colors.primary],
          inverseColors: true,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      stroke: {
        dashArray: 3
      },
      series: [78],
      labels: ['رشد']
    };

  if (typeof growthRadialChartEl !== undefined && growthRadialChartEl !== null) {
    const growthRadialChart = new ApexCharts(growthRadialChartEl, growthRadialChartConfig);
    growthRadialChart.render();
  }


    // ⭐️⭐️ تعریف این متغیر حیاتی است ⭐️⭐️
    // تأخیر بین انیمیشن خروج و انیمیشن ورود (کمتر از سرعت انیمیشن)
    const EXIT_ANIMATION_DELAY = 400;

    // ⭐️ تابع کمکی: محاسبه میانگین فقط برای مقادیر غیر صفر ⭐️
    const calculateNonZeroAverage = (series) => {
        if (!Array.isArray(series) || series.length === 0) {
            return 0;
        }

        let sum = 0;
        let count = 0;

        series.forEach(value => {
            // اطمینان از اینکه مقدار عدد است و صفر نیست (برای محاسبه میانگین واقعی)
            if (typeof value === 'number' && value !== 0) {
                sum += value;
                count += 1;
            }
        });

        if (count === 0) {
            return 0;
        }

        return Math.round(sum / count); // گرد کردن
    };

    // ⭐️ نمودار جدید: هزینه/درآمد/انتقال سالانه (Annual Chart)
    // --------------------------------------------------------------------
    const annualExpenseChartEl = document.querySelector('#annualExpenseChart');

    if (annualExpenseChartEl) {
        // ⭐️ متغیرها و المان‌ها را در بالاترین سطح تعریف می‌کنیم ⭐️
        const yearKindSelect = document.getElementById('yearkind');
        let annualChartInstance = null; // نمونه نمودار برای به‌روزرسانی

        // ⭐️ المان HTML برای نمایش میانگین (ID: annualAverageValue) ⭐️
        const averageEl = document.getElementById('annualAverageValue');

        // تابع نهایی و فوق ایمن برای پاکسازی و اعتبارسنجی رشته
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

        // ⭐️ تابع مرکزی برای ایجاد/به‌روزرسانی تنظیمات نمودار ⭐️
        const getChartConfig = (labels, series, kind = 'E') => {

            let color = config.colors.danger; // E (هزینه) -> قرمز
            let name = 'هزینه';

            if (kind === 'I') {
                color = config.colors.success; // I (درآمد) -> سبز
                name = 'درآمد';
            } else if (kind === 'T') {
                color = config.colors.info; // T (انتقال) -> آبی
                name = 'انتقال';
            }

            return {
                chart: {
                    height: 275,
                    type: 'bar',
                    toolbar: { show: true },

                    // ⭐️ تنظیمات انیمیشن برای ورود و خروج نرم ⭐️
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
                dataLabels: { enabled: false }, // غیرفعال کردن نمایش مبلغ روی میله
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

        // ⭐️ تابع AJAX برای دریافت و به‌روزرسانی داده‌ها (با انیمیشن تأخیری) ⭐️
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

            // 1. ابتدا داده‌های جدید را از سرور دریافت می‌کنیم.
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // ⭐️⭐️ محاسبه و نمایش میانگین ⭐️⭐️
                    const average = calculateNonZeroAverage(data.series);
                    const formattedAverage = average.toLocaleString('fa-IR');

                    // ⭐️⭐️ تغییر کلیدی: اضافه کردن عبارت ثابت قبل از مقدار ⭐️⭐️
                    const fullText = `میانگین ماهانه: ${formattedAverage} ریال`;

                    if (averageEl) {
                        // اگر المان فقط برای نمایش متن بود، کل متن را جایگزین می‌کنیم
                        averageEl.textContent = fullText;
                    } else {
                        console.warn("Element with ID 'annualAverageValue' not found.");
                    }

                    // تعداد ماه‌ها (میله‌ها) را از تنظیمات نمودار می‌گیریم
                    const currentDataLength = annualChartInstance.w.config.xaxis.categories.length;

                    // ساخت یک آرایه خالی (همه صفر) به اندازه تعداد ماه‌ها
                    const emptySeries = Array(currentDataLength).fill(0);

                    // ⭐️ مرحله ۱: انیمیشن خروج (پایین رفتن میله‌های قدیمی) ⭐️
                    // تغییر داده‌ها به صفر
                    annualChartInstance.updateOptions({
                        series: [{
                            name: annualChartInstance.w.config.series[0].name,
                            data: emptySeries
                        }]
                    }, false, true);

                    // ⭐️ مرحله ۲: تأخیر و انیمیشن ورود (بالا آمدن میله‌های جدید) ⭐️
                    setTimeout(() => {
                        // پس از پایان انیمیشن خروج، داده‌ها، نام و رنگ جدید را تزریق می‌کنیم.
                        annualChartInstance.updateOptions({
                            colors: [newColor],
                            series: [{
                                name: newName,
                                data: data.series // داده‌های واقعی جدید
                            }]
                        }, false, true);

                    }, EXIT_ANIMATION_DELAY); // تأخیر
                })
                .catch(error => {
                    console.error('Error fetching annual chart data:', error);
                });
        }

        // ⭐️ منطق رندر اولیه نمودار ⭐️
        if (typeof ApexCharts !== 'undefined') {
            const rawLabels = annualExpenseChartEl.getAttribute('data-labels');
            const rawSeries = annualExpenseChartEl.getAttribute('data-series');

            const chartLabels = parseChartData(rawLabels);
            const chartSeries = parseChartData(rawSeries);

            try {
                 if (chartLabels.length > 0 && chartSeries.length > 0) {
                    // محاسبه و نمایش میانگین اولیه (هزینه)
                    const initialAverage = calculateNonZeroAverage(chartSeries);
                    const formattedInitialAverage = initialAverage.toLocaleString('fa-IR');
                    const initialFullText = `میانگین ماهانه: ${formattedInitialAverage} ریال`;

                    if (averageEl) {
                        averageEl.textContent = initialFullText; // ⭐️⭐️ به‌روزرسانی شده ⭐️⭐️
                    }
                    // ساخت تنظیمات اولیه (نوع 'E')
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

        // ⭐️ شنونده رویداد منوی کشویی ⭐️
        if (yearKindSelect) {
            yearKindSelect.addEventListener('change', function() {
                const selectedKind = this.value;
                fetchAndUpdateAnnualChart(selectedKind);
            });
        }
    }
    // --------------------------------------------------------------------

    // ⭐️⭐️ بلوک: گزارش ماهانه (Monthly Report) ⭐️⭐️
    // --------------------------------------------------------------------
    const monthlyReportCardEl = document.querySelector('#monthlyReportCard');

    if (monthlyReportCardEl) {
        const monthKindSelect = document.getElementById('monthkind');
        const monthlyTotalEl = document.getElementById('monthlyTotalValue');
        const averageDayEl = document.getElementById('averageDay');
        const categoryListEl = document.getElementById('monthlyCategoryList');

        // ⭐️ تابع کمکی برای تعیین رنگ نوار بر اساس نوع تراکنش ⭐️
        const getProgressBarColor = (category, kind) => {
            // منطق عمومی بر اساس نوع تراکنش
            switch (kind) {
                case 'E':
                    return 'bg-danger'; // هزینه (شامل سرمایه‌گذاری): قرمز
                case 'I':
                    return 'bg-success'; // درآمد: سبز
                case 'T':
                    return 'bg-info'; // انتقال: آبی
                default:
                    return 'bg-secondary'; // پیش فرض
            }
        }

        // ⭐️ تابع کمکی برای ساخت HTML لیست دسته‌بندی‌ها ⭐️
        // ⭐️ تابع کمکی برای ساخت HTML لیست دسته‌بندی‌ها ⭐️
        const generateCategoryHtml = (categories, currentKind) => {
            let html = '<ul class="p-0 m-0">';

            if (Object.keys(categories).length === 0) {
                // ... (کد HTML برای تراکنش ثبت نشده) ...
                html += `<div class="card-body pb-5 d-flex flex-column justify-content-center align-items-center" style="margin-top: 96px">
                    <h6>هنوز هیچ تراکنشی ثبت نشده است.</h6>
                    <p class="text-muted">برای اضافه کردن تراکنش، <a href="{% url 'transactions' %}">اینجا</a> کلیک کنید</p>
                  </div>`;
            } else {
                // توجه: در API جدید، هر دسته‌بندی شامل [amount, percent, category_id] است.
                for (const [categoryName, dataList] of Object.entries(categories)) {
                    const amount = dataList[0];
                    const percent = dataList[1];
                    const categoryId = dataList[2]; // ⭐️⭐️ عنصر سوم: Category ID ⭐️⭐️

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

        // ⭐️ تابع AJAX برای دریافت و به‌روزرسانی داده‌های ماهانه ⭐️
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
                    // بلوک try...catch برای شناسایی دقیق خطای رندر JS
                    try {
                        // 1. به‌روزرسانی مجموع ماهانه
                        if (monthlyTotalEl) {
                            monthlyTotalEl.innerHTML = `${data.total_amount} <small class="text-muted fs-5">ریال</small>`;
                        }

                        // 2. به‌روزرسانی میانگین روزانه
                        if (averageDayEl) {
                            averageDayEl.textContent = `میانگین روزانه: ${data.average_daily} ریال`;
                        }

                        // 3. به‌روزرسانی لیست دسته‌بندی‌ها (ارسال 'kind' جدید)
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

        // منطق رندر اولیه میانگین روزانه (هنگام بارگذاری صفحه)
        const initialRenderAverageDay = () => {
            try {
                // مقادیر خام را از Data Attributes می‌خوانیم (بدون جداکننده)
                const initialTotalRaw = parseFloat(monthlyReportCardEl.getAttribute('data-initial-total')) || 0;
                const daysPassed = parseInt(monthlyReportCardEl.getAttribute('data-days-passed')) || 1;

                let averageDaily = 0;

                if (daysPassed > 0 && initialTotalRaw > 0) {
                    // توجه: اگر میانگین را بر اساس روزهای فعال محاسبه می‌کنید، باید
                    // active_days_count را به عنوان یک data-attribute جدید اضافه کنید
                    // و از آن به جای daysPassed در اینجا استفاده کنید.
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

        // ⭐️ اجرای توابع در هنگام بارگذاری صفحه ⭐️

        // 1. نمایش میانگین اولیه
        initialRenderAverageDay();

        // ⭐️ شنونده رویداد منوی کشویی ⭐️
        if (monthKindSelect) {
            monthKindSelect.addEventListener('change', function() {
                const selectedKind = this.value;
                fetchAndUpdateMonthlyReport(selectedKind);
            });
        }
    }
    // --------------------------------------------------------------------
})();