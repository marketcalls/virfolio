Below is an application design and requirements outline for VirFolio, a Flask-based virtual portfolio tracker for US and Indian stocks. This specification is intended for a prompt engineer or development team to deliver a modern, interactive, and extensible web application.

***

### Application Design Overview

- **Backend Framework:** Flask (Python)
- **Database:** SQLite using Flask SQLAlchemy ORM
- **Frontend:** Tailwind CSS + DaisyUI for rapid, beautiful UI development
- **Charts and Visualization:** Plotly
- **Market Data:** Yfinance for US and Indian stocks

***

### Core Pages & Features

#### Home Page
- Modern, visually engaging design inspired by the Supabase homepage (clean hero section, animated gradients, concise explanation of VirFolio).
- “Get Started”, “Login”, and “Sign Up” CTA buttons.
- Feature highlights, screenshots, and quick metrics visualizations.

#### Registration & Login
- Flask-login/session-based authentication.
- Registration with email/password, data validation, and password security.
- Login form with error handling and success feedback.

#### Dashboard
- Interactive summary of total user wealth, asset breakdown, and gains/losses.
- Dynamic Plotly charts for allocation, sector/country breakdown, and performance vs. benchmarks.
- Quick-glance cards for top gainers/losers, currency impact, daily change.

#### Portfolio & Holdings Management
- CRUD for stock positions (Add/Edit/Delete), supporting both US and Indian equities.
- Real-time price/fundamental data via Yfinance on demand.
- Editable model portfolios and custom asset tags.
- Table views with filters for country, sector, risk, and performance metrics.
- Detailed metrics per holding: market value, invested cost, absolute & annualized return, realized/unrealized gains.

#### Advanced Analytics
- Additional charts for sector exposures, historical equity curve, currency influences, and risk metrics.
- Visual comparison with indices or custom benchmarks.

#### Additional Functionalities
- Multi-portfolio support (track several virtual portfolios per user).
- Import/export of holdings via CSV/JSON.
- Investment insights and tips, optionally AI-powered.
- Basic notifications system for significant movements.

***

### Technical & Structural Requirements

#### Project Structure
- Modular blueprint architecture (separate apps for auth, portfolio, analytics, etc.).
- `app.py` or `run.py` as the entry point.
- `/models` for ORM model definitions (User, Portfolio, Position).
- `/templates` for Jinja2 HTML templates.
- `/static` for CSS (Tailwind), JS (Plotly), images, favicon.
- `/forms` for WTForms-backed registration/login inputs.
- `/routes` or `/views` for core page routing.
- `requirements.txt` for dependencies.

#### Database Schema (High-Level)
- Users: id, name/email, password_hash.
- Portfolios: id, user_id, name, base_currency.
- Positions: id, portfolio_id, stock_ticker, exchange, quantity, buy_price, buy_date, notes.

#### Integrations
- Tailwind CSS and DaisyUI via npm or CDN for rapid frontend styling.
- Plotly.js for chart embedding or Flask-Plotly wrapper for cross-framework charts.
- Yfinance client for real-time API lookups and historical data fetching.
- Optionally, Flask-WTF for robust form validation.

#### UI/UX
- Responsive layouts for mobile and desktop.
- Light/dark theme support.
- DaisyUI components for navbar, cards, tables, modals, forms, alerts.

***

### Prompt Engineer Tasks

- Implement reusable Jinja2 templates with Tailwind/DaisyUI classes.
- Build modular Flask blueprints (authentication, dashboard, analytics, etc.).
- Integrate Plotly for wealth charts and dynamic portfolio analytics.
- Wire up SQLite models with SQLAlchemy: user, portfolios, holdings.
- Connect to Yfinance for fetching and updating stock data.
- Develop modern, interactive, and simple-to-navigate homepage inspired by Supabase.

***

### Stretch Features (for Improvement)

- Social login and user avatars.
- In-app notifications for news and price breaks.
- Performance reports and downloadable PDFs.
- Global search for tickers and quick addition.
- AI-powered insights for best performing sectors/stock tips.

***

This document gives a self-contained, actionable blueprint for building, styling, and scaling the VirFolio portfolio tracker—ready for a prompt engineer or full-stack developer.

[1](https://www.geeksforgeeks.org/python/single-page-portfolio-using-flask/)
[2](https://www.linkedin.com/pulse/building-portfolio-website-flask-atomixweb-1shzf)
[3](https://www.meritshot.com/flask-application-structure/)
[4](https://empiricinfotech.com/blogs/flask-project-ideas)
[5](https://dev.to/cre8stevedev/building-a-full-stack-web-application-using-flask-python-web-framework-part-one-5b1i)
[6](https://github.com/dmdhrumilmistry/Flask-Portfolio)
[7](https://www.reddit.com/r/Python/comments/ho6jpm/wip_made_a_stocks_portfolio_manager_website_using/)