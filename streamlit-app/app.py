import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyodbc
from datetime import datetime, timedelta
import io
from typing import Dict, List, Optional
import numpy as np
import warnings

# Suppress the pandas SQLAlchemy warning since we're using pyodbc intentionally
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy connectable.*')

# Page configuration
st.set_page_config(
    page_title="Kyle Tran's Real Estate Investment Trust",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with MRK Water Analytics styling
st.markdown("""
<style>
    /* Typography and base styles */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0C223A;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: transparent;
        border-radius: 4px;
        color: #666;
        font-size: 14px;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #F47C20;
        border-bottom: 2px solid #F47C20;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
        transition: transform 0.2s;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .kpi-title {
        font-size: 14px;
        color: #666;
        font-weight: 600;
        margin: 0;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #0C223A;
        margin: 10px 0 5px 0;
    }
    
    .kpi-comparison {
        font-size: 13px;
        color: #666;
        margin: 5px 0;
    }
    
    .kpi-target {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #eee;
        font-size: 13px;
    }
    
    /* Trend indicators */
    .trend-indicator {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 14px;
        font-weight: 600;
    }
    
    .trend-up {
        color: #00aa00;
    }
    
    .trend-down {
        color: #ff4444;
    }
    
    .trend-neutral {
        color: #ff8800;
    }
    
    /* Status indicators */
    .status-good {
        color: #00aa00;
        font-weight: 600;
    }
    
    .status-warning {
        color: #ff8800;
        font-weight: 600;
    }
    
    .status-alert {
        color: #ff4444;
        font-weight: 600;
    }
    
    /* Alert section */
    .alert-section {
        background: #fff5f5;
        border-left: 4px solid #ff4444;
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .alert-header {
        font-weight: bold;
        color: #ff4444;
        margin-bottom: 10px;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .alert-item {
        padding: 5px 0;
        color: #666;
        font-size: 14px;
    }
    
    /* Financial card styling */
    .financial-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    
    .financial-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #0C223A;
    }
    
    .financial-detail {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    .financial-detail:last-child {
        border-bottom: none;
    }
    
    .financial-label {
        color: #666;
        font-size: 14px;
    }
    
    .financial-value {
        font-weight: bold;
        color: #0C223A;
        font-size: 14px;
    }
    
    /* Section styling */
    .section {
        background-color: white;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1d391kg .stSidebar {
        background-color: #333;
    }
    
    .css-1d391kg .stSidebar > div {
        background-color: #333;
        color: white;
    }
    
    /* Sidebar text color */
    .css-1d391kg .stSidebar label {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #F47C20;
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 4px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #d56617;
    }
    
    /* Debug info styling */
    .debug-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
    
    /* Data table styling */
    .dataframe {
        font-size: 14px;
    }
    
    .dataframe thead th {
        background-color: #f5f5f5;
        font-weight: bold;
        text-align: left;
        padding: 10px;
    }
    
    .dataframe tbody td {
        padding: 8px;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #F47C20 !important;
    }
</style>
""", unsafe_allow_html=True)

class RealEstateDashboard:
    def __init__(self):
        self.conn = None
        self.current_user = None
        
    def connect_to_database(self):
        """Connect to the Azure SQL Server MultifamilyRealEstateDB database"""
        server = "kyletristentran.database.windows.net"
        database = "MultifamilyRealEstateDB"
        username = "kyletristentran"
        password = "Tran1105"
        driver = "ODBC Driver 17 for SQL Server"
        
        conn_str = (
            f"Driver={{{driver}}};"
            f"Server=tcp:{server},1433;"
            f"Database={database};"
            f"Uid={username};"
            f"Pwd={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        
        try:
            self.conn = pyodbc.connect(conn_str)
            return True
        except pyodbc.Error as e:
            st.error(f"❌ Error connecting to database: {str(e)}")
            return False
    
    def disconnect_from_database(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def test_database_connection(self):
        """Test database connection using pyodbc and show detailed results"""
        st.write("🔍 **Testing Database Connection...**")
        
        # Connection parameters
        server = "kyletristentran.database.windows.net"
        database = "MultifamilyRealEstateDB"
        username = "kyletristentran"
        password = "Tran1105"
        driver = "ODBC Driver 17 for SQL Server"
        
        # Show connection details (without password)
        st.write(f"**Server:** {server}")
        st.write(f"**Database:** {database}")
        st.write(f"**Username:** {username}")
        st.write(f"**Driver:** {driver}")
        
        # Construct connection string
        conn_str = (
            f"Driver={{{driver}}};"
            f"Server=tcp:{server},1433;"
            f"Database={database};"
            f"Uid={username};"
            f"Pwd={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        
        try:
            st.write("⏳ Attempting to connect with pyodbc...")
            test_conn = pyodbc.connect(conn_str)
            st.success("✅ **Database connection successful!**")
            
            # Test a simple query
            cursor = test_conn.cursor()
            cursor.execute("SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            result = cursor.fetchone()
            st.write(f"📊 Found {result[0]} tables in database")
            
            # Test specific tables
            st.write("**Checking key tables:**")
            tables_to_check = ['Properties', 'MonthlyFinancials', 'Units', 'Tenants']
            
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM dbo.{table}")
                    count = cursor.fetchone()[0]
                    st.write(f"✅ {table}: {count} records")
                except Exception as e:
                    st.write(f"❌ {table}: Error - {str(e)}")
            
            test_conn.close()
            return True
            
        except pyodbc.Error as e:
            st.error(f"❌ **Database connection failed!**")
            st.error(f"Error: {str(e)}")
            
            # Provide troubleshooting tips
            error_msg = str(e).lower()
            if "login failed" in error_msg:
                st.warning("**Possible authentication issues:**")
                st.write("1. Check if username/password are correct")
                st.write("2. Verify the user has permissions to access this database")
                st.write("3. Check if your IP address is allowed in Azure SQL firewall rules")
            elif "timeout" in error_msg:
                st.warning("**Connection timeout issues:**")
                st.write("1. Verify your network connection")
                st.write("2. Check if the server name is correct")
                st.write("3. Check if the Azure SQL server is running")
            
            return False
        except Exception as e:
            st.error(f"❌ **Unexpected error:** {str(e)}")
            return False
    
    def simple_authentication(self):
        """Simple authentication system"""
        st.sidebar.markdown('<h3 style="color: white;">🔐 Login</h3>', unsafe_allow_html=True)
        
        # Check if already logged in
        if st.session_state.get('authenticated', False):
            st.sidebar.success(f"Logged in as: {st.session_state.get('username', 'Unknown')}")
            if st.sidebar.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.rerun()
            return True, st.session_state.get('username', 'Unknown')
        
        # Login form
        username = st.sidebar.text_input("Username", placeholder="Enter username")
        password = st.sidebar.text_input("Password", type="password", placeholder="Enter password")
        
        if st.sidebar.button("🔑 Login"):
            if username and password:
                # Simple credential check
                if (username == "admin" and password == "admin123") or (username == "kyle" and password == "kyle123"):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.sidebar.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Invalid credentials")
            else:
                st.sidebar.warning("⚠️ Please enter both username and password")
        
        # Show demo credentials
        st.sidebar.info("**Demo Credentials:**\n- admin / admin123\n- kyle / kyle123")
        
        return False, None
    
    def get_portfolio_kpis(self, year: int) -> Dict:
        """Get key portfolio metrics for the dashboard"""
        if not self.conn:
            return {}
        
        try:
            # Current year YTD metrics
            current_query = """
            SELECT 
                ISNULL(SUM(TotalIncome), 0) as total_revenue,
                ISNULL(SUM(TotalExpenses), 0) as total_expenses,
                ISNULL(SUM(NOI), 0) as total_noi,
                CASE 
                    WHEN AVG(Vacancy) > 100 THEN AVG(Vacancy) / 100
                    WHEN AVG(Vacancy) < 0 THEN 0
                    ELSE ISNULL(AVG(Vacancy), 0)
                END as avg_vacancy,
                COUNT(DISTINCT PropertyID) as property_count
            FROM dbo.MonthlyFinancials mf
            WHERE YEAR(ReportingMonth) = ? AND MONTH(ReportingMonth) <= MONTH(GETDATE())
            """
            
            current_df = pd.read_sql(current_query, self.conn, params=[year])
            
            # Previous year same period for variance calculation
            prev_year_query = """
            SELECT 
                ISNULL(SUM(NOI), 0) as prev_noi,
                ISNULL(SUM(TotalIncome), 0) as prev_revenue
            FROM dbo.MonthlyFinancials mf
            WHERE YEAR(ReportingMonth) = ? AND MONTH(ReportingMonth) <= MONTH(GETDATE())
            """
            
            prev_df = pd.read_sql(prev_year_query, self.conn, params=[year-1])
            
            # Property values for portfolio value calculation
            property_query = """
            SELECT ISNULL(SUM(PurchasePrice), 0) as total_portfolio_value
            FROM dbo.Properties
            """
            
            portfolio_df = pd.read_sql(property_query, self.conn)
            
            # Calculate variances
            current_noi = current_df['total_noi'].iloc[0] or 0
            prev_noi = prev_df['prev_noi'].iloc[0] or 0
            noi_variance = ((current_noi - prev_noi) / prev_noi * 100) if prev_noi != 0 else 0
            
            current_revenue = current_df['total_revenue'].iloc[0] or 0
            prev_revenue = prev_df['prev_revenue'].iloc[0] or 0
            revenue_variance = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue != 0 else 0
            
            # Ensure vacancy is between 0 and 100
            avg_vacancy = current_df['avg_vacancy'].iloc[0] or 0
            avg_vacancy = min(max(avg_vacancy, 0), 100)
            
            return {
                'total_portfolio_value': portfolio_df['total_portfolio_value'].iloc[0] or 0,
                'total_revenue': current_revenue,
                'total_expenses': current_df['total_expenses'].iloc[0] or 0,
                'total_noi': current_noi,
                'avg_vacancy': avg_vacancy,
                'property_count': current_df['property_count'].iloc[0] or 0,
                'noi_variance': noi_variance,
                'revenue_variance': revenue_variance,
                'prev_noi': prev_noi,
                'prev_revenue': prev_revenue
            }
            
        except Exception as e:
            st.error(f"Error fetching KPIs: {str(e)}")
            return {}
    
    def get_monthly_performance(self, year: int) -> pd.DataFrame:
        """Get monthly performance data for charts"""
        if not self.conn:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT 
                ReportingMonth,
                ISNULL(SUM(TotalIncome), 0) as Revenue,
                ISNULL(SUM(TotalExpenses), 0) as Expenses,
                ISNULL(SUM(NOI), 0) as NOI,
                ISNULL(SUM(CashFlow), 0) as CashFlow,
                CASE 
                    WHEN AVG(Vacancy) > 100 THEN AVG(Vacancy) / 100
                    WHEN AVG(Vacancy) < 0 THEN 0
                    ELSE ISNULL(AVG(Vacancy), 0)
                END as Vacancy
            FROM dbo.MonthlyFinancials
            WHERE YEAR(ReportingMonth) = ?
            GROUP BY ReportingMonth
            ORDER BY ReportingMonth
            """
            
            df = pd.read_sql(query, self.conn, params=[year])
            if not df.empty:
                df['ReportingMonth'] = pd.to_datetime(df['ReportingMonth'])
            return df
            
        except Exception as e:
            st.error(f"Error fetching monthly performance: {str(e)}")
            return pd.DataFrame()
    
    # Removed create_kpi_card method - using native Streamlit metrics instead
    
    def get_property_details(self, year):
        """Fetch detailed property information including financials"""
        try:
            if not self.conn:
                return pd.DataFrame()
            
            query = """
            SELECT 
                p.PropertyID,
                p.PropertyName,
                p.PurchasePrice,
                p.UnitCount as TotalUnits,
                COALESCE(SUM(mf.TotalIncome), 0) as TotalRevenue,
                COALESCE(SUM(mf.TotalExpenses), 0) as TotalExpenses,
                COALESCE(SUM(mf.NOI), 0) as TotalNOI,
                CASE 
                    WHEN AVG(mf.Vacancy) > 100 THEN AVG(mf.Vacancy) / 100
                    WHEN AVG(mf.Vacancy) < 0 THEN 0
                    ELSE COALESCE(AVG(mf.Vacancy), 0)
                END as AvgVacancy,
                COUNT(DISTINCT mf.ReportingMonth) as MonthsReported
            FROM dbo.Properties p
            LEFT JOIN dbo.MonthlyFinancials mf ON p.PropertyID = mf.PropertyID
                AND YEAR(mf.ReportingMonth) = ?
            GROUP BY p.PropertyID, p.PropertyName, p.PurchasePrice, p.UnitCount
            ORDER BY p.PropertyName
            """
            
            df = pd.read_sql(query, self.conn, params=[year])
            
            # Additional safety check: ensure vacancy is between 0 and 100
            if not df.empty and 'AvgVacancy' in df.columns:
                df['AvgVacancy'] = df['AvgVacancy'].clip(0, 100)
            
            return df
            
        except Exception as e:
            st.error(f"Error fetching property details: {str(e)}")
            return pd.DataFrame()
    
    def create_alerts(self, kpis: Dict):
        """Create alert section if needed"""
        alerts = []
        
        # Check NOI performance
        if kpis.get('noi_variance', 0) < -10:
            alerts.append(f"NOI decreased by {abs(kpis['noi_variance']):.1f}% compared to last year")
        
        # Check vacancy
        if kpis.get('avg_vacancy', 0) > 10:
            alerts.append(f"Average vacancy ({kpis['avg_vacancy']:.1f}%) is above 10% target")
        
        # Check revenue
        if kpis.get('revenue_variance', 0) < -5:
            alerts.append(f"Revenue decreased by {abs(kpis['revenue_variance']):.1f}% compared to last year")
        
        if alerts:
            alert_items = "".join([f'<div class="alert-item">• {alert}</div>' for alert in alerts])
            return f"""
            <div class="alert-section">
                <div class="alert-header">⚠️ Critical Alerts</div>
                {alert_items}
            </div>
            """
        return ""
    
    # Removed create_financial_card method - using native Streamlit components instead

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Kyle Tran\'s Real Estate Investment Trust</h1>', unsafe_allow_html=True)
    
    # Initialize dashboard
    dashboard = RealEstateDashboard()
    
    # Sidebar controls
    st.sidebar.markdown('<h3 style="color: white;">Real Estate Analytics</h3>', unsafe_allow_html=True)
    
    # Debug mode toggle
    debug_mode = st.sidebar.checkbox("🐛 Debug Mode", value=False)
    
    if debug_mode:
        st.sidebar.markdown("---")
        st.sidebar.markdown('<h4 style="color: white;">🔧 Debug Tools</h4>', unsafe_allow_html=True)
        
        if st.sidebar.button("🧪 Test Database Connection"):
            with st.container():
                st.header("Database Connection Test")
                dashboard.test_database_connection()
        
        st.sidebar.markdown("---")
    
    # Authentication
    is_authenticated, username = dashboard.simple_authentication()
    
    if not is_authenticated:
        st.info("👋 Please log in using the sidebar to access the dashboard")
        return
    
    # Connect to database
    if not dashboard.connect_to_database():
        st.error("Failed to connect to database. Please check your connection.")
        return
    
    # Year selector
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h4 style="color: white;">📊 Dashboard Controls</h4>', unsafe_allow_html=True)
    current_year = datetime.now().year
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=list(range(current_year-5, current_year+1)),
        index=5
    )
    
    # Set default values (removed settings section for simplicity)
    noi_target = 50000
    occupancy_target = 95.0
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Main content with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Performance Overview",
        "Portfolio Analysis",
        "Financial Trends",
        "Property Details",
        "Data Management"
    ])
    
    try:
        # Get data
        with st.spinner("Loading dashboard data..."):
            kpis = dashboard.get_portfolio_kpis(selected_year)
            monthly_data = dashboard.get_monthly_performance(selected_year)
        
        # Tab 1: Performance Overview
        with tab1:
            # Alerts
            alert_html = dashboard.create_alerts(kpis)
            if alert_html:
                st.markdown(alert_html, unsafe_allow_html=True)
            
            # KPI Cards
            st.markdown("### Key Performance Indicators")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Portfolio Value",
                    value=f"${kpis.get('total_portfolio_value', 0):,.0f}",
                    delta="On Track"
                )
            
            with col2:
                noi_comparison = kpis.get('total_noi', 0) - kpis.get('prev_noi', 0)
                st.metric(
                    label="YTD NOI",
                    value=f"${kpis.get('total_noi', 0):,.0f}",
                    delta=f"${noi_comparison:,.0f}",
                    delta_color="normal" if noi_comparison >= 0 else "inverse"
                )
            
            with col3:
                revenue_comparison = kpis.get('total_revenue', 0) - kpis.get('prev_revenue', 0)
                st.metric(
                    label="YTD Revenue",
                    value=f"${kpis.get('total_revenue', 0):,.0f}",
                    delta=f"${revenue_comparison:,.0f}",
                    delta_color="normal" if revenue_comparison >= 0 else "inverse"
                )
            
            with col4:
                vacancy_target = 5.0  # 5% vacancy target
                st.metric(
                    label="Avg Vacancy",
                    value=f"{kpis.get('avg_vacancy', 0):.1f}%",
                    delta="Good" if kpis.get('avg_vacancy', 0) <= vacancy_target else "Above Target",
                    delta_color="normal" if kpis.get('avg_vacancy', 0) <= vacancy_target else "inverse"
                )
            
            # Financial Snapshot
            st.markdown("### Financial Snapshot")
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container():
                    st.markdown("**Current Period**")
                    st.metric("Total Revenue", f"${kpis.get('total_revenue', 0):,.0f}")
                    st.metric("Total Expenses", f"${kpis.get('total_expenses', 0):,.0f}")
                    st.metric("Net Operating Income", f"${kpis.get('total_noi', 0):,.0f}")
                    st.metric("Properties", f"{kpis.get('property_count', 0)}")
            
            with col2:
                with st.container():
                    st.markdown("**Year-over-Year Comparison**")
                    st.metric("NOI Change", f"{kpis.get('noi_variance', 0):+.1f}%")
                    st.metric("Revenue Change", f"{kpis.get('revenue_variance', 0):+.1f}%")
                    st.metric("Avg Vacancy", f"{kpis.get('avg_vacancy', 0):.1f}%")
                    st.metric("Performance", "Strong" if kpis.get('noi_variance', 0) > 5 else "Stable")
        
        # Tab 2: Portfolio Analysis
        with tab2:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("📊 Monthly Performance Trends")
            
            if not monthly_data.empty:
                # Create dual-axis chart
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Revenue & Expenses', 'NOI & Cash Flow'),
                    vertical_spacing=0.15
                )
                
                # Revenue & Expenses
                fig.add_trace(
                    go.Scatter(x=monthly_data['ReportingMonth'], y=monthly_data['Revenue'],
                             name='Revenue', line=dict(color='#0C223A', width=3)),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=monthly_data['ReportingMonth'], y=monthly_data['Expenses'],
                             name='Expenses', line=dict(color='#F47C20', width=3)),
                    row=1, col=1
                )
                
                # NOI & Cash Flow
                fig.add_trace(
                    go.Bar(x=monthly_data['ReportingMonth'], y=monthly_data['NOI'],
                          name='NOI', marker_color='#0C223A'),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=monthly_data['ReportingMonth'], y=monthly_data['CashFlow'],
                             name='Cash Flow', line=dict(color='#F47C20', width=2)),
                    row=2, col=1
                )
                
                fig.update_layout(height=600, showlegend=True, hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No monthly data available for the selected year")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 3: Financial Trends
        with tab3:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("📈 Financial Trends Analysis")
            
            if not monthly_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Vacancy trend
                    fig_vac = px.line(monthly_data, x='ReportingMonth', y='Vacancy',
                                    title='Vacancy Rate Trend',
                                    color_discrete_sequence=['#0C223A'])
                    fig_vac.add_hline(y=5.0, line_dash="dash", 
                                    line_color="red", annotation_text="Target")
                    fig_vac.update_layout(height=350)
                    st.plotly_chart(fig_vac, use_container_width=True)
                
                with col2:
                    # NOI margin
                    monthly_data['NOI_Margin'] = (monthly_data['NOI'] / monthly_data['Revenue'] * 100)
                    fig_margin = px.bar(monthly_data, x='ReportingMonth', y='NOI_Margin',
                                      title='NOI Margin %',
                                      color_discrete_sequence=['#F47C20'])
                    fig_margin.update_layout(height=350)
                    st.plotly_chart(fig_margin, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 4: Property Details
        with tab4:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("🏢 Property Portfolio Details")
            
            # Fetch property details
            property_data = dashboard.get_property_details(selected_year)
            
            if not property_data.empty:
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Properties", len(property_data))
                with col2:
                    st.metric("Total Units", f"{property_data['TotalUnits'].sum():,}")
                with col3:
                    st.metric("Portfolio Revenue", f"${property_data['TotalRevenue'].sum():,.0f}")
                with col4:
                    st.metric("Portfolio NOI", f"${property_data['TotalNOI'].sum():,.0f}")
                
                st.markdown("---")
                
                # Property cards
                st.markdown("### Individual Property Performance")
                
                # Create columns for property cards (2 per row)
                for i in range(0, len(property_data), 2):
                    cols = st.columns(2)
                    
                    for j, col in enumerate(cols):
                        if i + j < len(property_data):
                            property = property_data.iloc[i + j]
                            
                            with col:
                                with st.container():
                                    st.markdown(f"#### {property['PropertyName']}")
                                    st.markdown(f"💰 **Purchase Price:** ${property['PurchasePrice']:,.0f}")
                                    
                                    # Property metrics
                                    metric_cols = st.columns(3)
                                    with metric_cols[0]:
                                        st.metric("Units", f"{int(property['TotalUnits']):,}")
                                    with metric_cols[1]:
                                        st.metric("Vacancy Rate", f"{property['AvgVacancy']:.1f}%")
                                    with metric_cols[2]:
                                        st.metric("Months Active", property['MonthsReported'])
                                    
                                    # Financial metrics
                                    st.markdown("**Financial Performance:**")
                                    financial_cols = st.columns(3)
                                    with financial_cols[0]:
                                        st.metric("Revenue", f"${property['TotalRevenue']:,.0f}")
                                    with financial_cols[1]:
                                        st.metric("Expenses", f"${property['TotalExpenses']:,.0f}")
                                    with financial_cols[2]:
                                        noi_color = "normal" if property['TotalNOI'] >= 0 else "inverse"
                                        st.metric("NOI", f"${property['TotalNOI']:,.0f}", 
                                                delta_color=noi_color)
                                    
                                    # NOI Margin if revenue > 0
                                    if property['TotalRevenue'] > 0:
                                        noi_margin = (property['TotalNOI'] / property['TotalRevenue']) * 100
                                        st.metric("NOI Margin", f"{noi_margin:.1f}%")
                                    
                                    st.markdown("---")
                
                # Export option
                st.markdown("### Export Property Data")
                csv = property_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Property Details as CSV",
                    data=csv,
                    file_name=f"property_details_{selected_year}.csv",
                    mime='text/csv'
                )
            else:
                st.warning("No property data available for the selected year.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tab 5: Data Management
        with tab5:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.subheader("📋 Monthly Performance Data")
            
            if not monthly_data.empty:
                # Format the data for display
                display_data = monthly_data.copy()
                display_data['ReportingMonth'] = display_data['ReportingMonth'].dt.strftime('%Y-%m')
                
                # Format numeric columns
                for col in ['Revenue', 'Expenses', 'NOI', 'CashFlow']:
                    display_data[col] = display_data[col].apply(lambda x: f"${x:,.2f}")
                display_data['Vacancy'] = display_data['Vacancy'].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(display_data, use_container_width=True, height=400)
                
                # Export options
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = monthly_data.to_csv(index=False)
                    st.download_button(
                        label="📊 Download Monthly Data (CSV)",
                        data=csv,
                        file_name=f"monthly_performance_{selected_year}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    if st.button("📋 Export KPI Summary"):
                        kpi_df = pd.DataFrame([kpis])
                        csv_kpi = kpi_df.to_csv(index=False)
                        st.download_button(
                            label="Download KPI Summary",
                            data=csv_kpi,
                            file_name=f"kpi_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if debug_mode:
            st.markdown("---")
            st.subheader("🐛 Debug Information")
            with st.expander("Show Debug Data"):
                st.write("**KPIs:**", kpis)
                st.write("**Monthly Data Shape:**", monthly_data.shape if not monthly_data.empty else "No data")
                st.write("**Session State:**", dict(st.session_state))
    
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        if debug_mode:
            st.write("**Full error details:**")
            st.exception(e)
    
    finally:
        # Clean up database connection
        dashboard.disconnect_from_database()

if __name__ == "__main__":
    main()