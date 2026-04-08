# Coffee Price Analysis Report

This report presents the findings of a data mining project analyzing Vietnamese news articles about coffee commodity prices. The project aimed to uncover trends, patterns, and insights into coffee price fluctuations over a 66-day period (January-March 2026).

---

## Executive Summary

- **Data Volume**: 2,875 news articles from 85 Vietnamese news sources
- **Extracted Records**: 496 articles with identifiable coffee prices (17.3%)
- **Analysis Period**: 66 days
- **Key Findings**:
  - Average coffee price: 100,782 đ/kg
  - Price range: 90,400 - 152,000 đ/kg
  - Price volatility: 12.1%
  - Overall price change: -6.9%

---

## Objectives

The primary goal of this project was to analyze coffee price trends in Vietnam by leveraging web scraping and data mining techniques. The analysis aimed to provide actionable insights for stakeholders in the coffee industry, including producers, traders, and policymakers.

---

## Methodology

1. **Data Collection**:
   - Scraped Vietnamese news websites using Scrapy.
   - Collected 2,875 articles mentioning coffee prices.

2. **Data Processing**:
   - Extracted price data from headlines and article content using regular expressions.
   - Cleaned and standardized data for analysis.

3. **Statistical Analysis**:
   - Performed descriptive statistics and time series analysis to identify trends and patterns.

4. **Visualization**:
   - Created charts and graphs to illustrate price movements and volatility.

5. **Reporting**:
   - Compiled findings into a comprehensive report.

---

## Key Insights

- **Price Trends**: Coffee prices showed a downward trend over the analysis period, with a 6.9% decrease in average price.
- **Volatility**: Prices exhibited moderate volatility, with a coefficient of variation of 12.1%.
- **Regional Differences**: Significant price variations were observed across different regions.
- **Market Dynamics**: External factors such as global market trends and domestic policies influenced price fluctuations.

---

## Visualizations

### Price Trend Over Time

![Price Trend](images/price_trend.png)

*Figure 1: Coffee price trend over the analysis period.*

### Price Distribution

![Price Distribution](images/price_distribution.png)

*Figure 2: Distribution of coffee prices.*

---

## Detailed Statistics

| Metric                  | Value          |
|-------------------------|----------------|
| Raw Articles Collected | 2,875          |
| Articles with Prices    | 496            |
| Extraction Success Rate | 17.3%          |
| Average Price           | 100,782 đ/kg   |
| Price Range             | 90,400 - 152,000 đ/kg |
| Price Volatility (CV)   | 12.1%          |
| Price Change (Period)   | -6.9%          |

---

## Recommendations

- **For Producers**: Focus on cost optimization to mitigate the impact of price volatility.
- **For Traders**: Leverage predictive analytics to anticipate price movements and adjust inventory strategies.
- **For Policymakers**: Implement measures to stabilize coffee prices and support small-scale farmers.

---

## Conclusion

This analysis highlights the importance of data-driven decision-making in the coffee industry. By understanding price trends and market dynamics, stakeholders can make informed decisions to enhance profitability and sustainability.

---

For further details, please refer to the full dataset and analysis scripts included in this repository.
