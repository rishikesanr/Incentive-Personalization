import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from time import sleep
import random

# Title
st.title("Monocle Incentive Personalization Platform!")

# Sidebar with icons (Data Sources, Data Models, Workspaces, Integration, Insights, Users)
st.sidebar.header("Menu")
menu = st.sidebar.radio("Choose a section", 
                        ("Data Sources", "Data Models", "Workspaces", "Integration", "Insights", "Users"), index=2)  # Default to "Workspaces"

# Placeholder for the happy emoji
happy_emoji = "😊"

# Data Sources Section
if menu == "Data Sources":
    st.header("Create a Data Source")
    
    # Input for Data Source Name
    data_source_name = st.text_input("Enter Data Source Name")

    # Data Source type selection
    data_source_type = st.selectbox("Select Data Source Type", 
                                    ("PostgreSQL", "MySQL", "Elasticsearch"))

    st.subheader(f"Enter credentials for {data_source_type}")
    
    # Input fields for credentials
    ip_address = st.text_input("IP Address", value="192.168.1.1")
    port = st.text_input("Port", value="5432")
    access_key = st.text_input("Access Key", value="************", type="password")
    database = st.text_input("Database Name", value="dummy_db")
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", value="password123", type="password")

    # Connect button
    connect_button = st.button("Connect")

    if connect_button:
        st.write(f"Connecting to {data_source_type} at {ip_address}:{port} ...")
        sleep(1)  # Simulate connection time
        st.success(f"Connected to {data_source_type} successfully!")

# Data Models Section
elif menu == "Data Models":
    st.header("Data Models")

    # Input for Data Source Name
    data_source_name = st.text_input("Enter Data Source Name")

    # Input for Data Model Name
    data_model_name = st.text_input("Enter Data Model Name")

    # Query input box
    query = st.text_area("Write your query", value="SELECT user_id, variant_name, exposed_at, "
                                                   "days_since_signup, loyalty_points, sign_up_incentive, "
                                                   "num_past_orders_14d, order_conversion, revenue, "
                                                   "num_past_clicked_emails_14d FROM customer_info")

    if st.button("Preview Query"):
        # Generating a random dataframe to simulate the query output
        data = {
            'user_id': [random.randint(1000, 9999) for _ in range(10)],
            'variant_name': [random.choice(['A', 'B']) for _ in range(10)],
            'exposed_at': pd.date_range('2023-09-01', periods=10).to_list(),
            'days_since_signup': [random.randint(1, 365) for _ in range(10)],
            'loyalty_points': [random.randint(0, 5000) for _ in range(10)],
            'sign_up_incentive': [random.choice([True, False]) for _ in range(10)],
            'num_past_orders_14d': [random.randint(0, 5) for _ in range(10)],
            'order_conversion': [round(random.uniform(0, 1), 2) for _ in range(10)],
            'revenue': [round(random.uniform(10.0, 1000.0), 2) for _ in range(10)],
            'num_past_clicked_emails_14d': [random.randint(0, 20) for _ in range(10)]
        }

        df = pd.DataFrame(data)
        st.write("Preview of the top 10 rows of your query:")
        st.dataframe(df.head(10))

    if st.button("Submit Data Model"):
        st.success(f"Data Model '{data_model_name}' submitted successfully!")

# Workspaces Section
elif menu == "Workspaces":
    st.header("Workspaces")

    # Input for Workspace Name and Data Model
    workspace_name = st.text_input("Enter Campaign Name")
    data_model_name_training = st.text_input("Enter Data Model for Training")
    data_model_name_inference = st.text_input("Enter Data Model for Inference")

    # Workspace creation options
    workspace_type = st.selectbox("Select Workspace Type", 
                                  ("Attract New Customers", "Attract All Customers"))

    if workspace_name and workspace_type and data_model_name_training:
        # Workspace details remain visible on the same page
        st.subheader(f"Campaign: {workspace_name} ({workspace_type})")

        if workspace_type == "Attract New Customers":
            st.write("Attract new customers who never placed an order before. Maximize CVR under budget!")
        
        elif workspace_type == "Attract All Customers":
            st.write("Improve frequency from new and return customers. Optimize CVR, Revenue, and Profits under budget!")
            
            # Options for Customer Incentive
            st.write("### Training Configuration:")
            customer_incentive = st.selectbox("Choose an incentive", 
                                          ("%", "Dollar Off", "Free Delivery"))
            if customer_incentive == "%":
                # Coupon strategy selection
                coupon_strategy = st.selectbox("Coupon Strategy", ("Custom", "Auto"))
                
                # If Custom is selected, allow entering custom coupons
                if coupon_strategy == "Custom":
                    custom_coupons = st.text_input("Enter coupon values (e.g., 0%, 10%, 15%)")
                    st.write(f"Selected Custom Coupons: {custom_coupons}%")
                  
            st.write("### Inferece Configuration:")
            campaign_freq = st.selectbox("Choose campaign frequency", 
                                           ("Hourly", "Daily", "Weekly"))
            campaign_length = st.selectbox("Choose campaign length", 
                                           ("1 month", "6 months", "1 year", "Auto"))
            
            # If "%" is selected for customer incentive
            if customer_incentive == "%":
                st.write("### Optimization Constraints:")
                
                # Percentage of users who receive coupons
                percent_coupons = st.slider("% of users who receive coupons", 0, 100, 50)
                st.write(f"Selected: {percent_coupons}% of users will receive coupons.")
                
            
            # If "Dollar Off" is selected for customer incentive
            elif customer_incentive == "Dollar Off":
                
                # Weekly budget option: Enter a value or choose no cap
                weekly_budget_option = st.selectbox("Average Weekly Budget", 
                                                ("Enter a number", "No cap on average weekly budget"))
                
                # If "Enter a number" is selected, allow entering the weekly budget value
                if weekly_budget_option == "Enter a number":
                    weekly_budget_value = st.number_input("Enter your weekly budget in dollars", min_value=0)
                    st.write(f"Weekly Budget: ${weekly_budget_value}")
                else:
                    st.write("No cap on average weekly budget.")
        
        # Start Promotion Button
        start_button = st.button("Start Promotion")

        # Simulate promotion starting when the button is clicked
        if start_button:
            st.write("Starting your promotion...")
            sleep(2)  # Simulate a delay for starting the promotion
            st.success(f"Promotion Started! {happy_emoji} Let's drive positive results together!")


# Insights Section
elif menu == "Insights":
    st.header("Overall Campaign Performance")

    # Generate random time-series data for before and after intervention for all campaigns
    dates = pd.date_range(start="2023-01-01", periods=10, freq="M")

    # Pre-intervention values (before Monocle stepped in)
    before_monocle = [41000, 42345, 41600, 41400, 42800]
    # Post-intervention values (after Monocle intervention)
    after_monocle = [60300, 62000, 61500, 64200, 65100]
    # Projected values without Monocle intervention
    projected_without_monocle = [41200, 38900, 40940, 42800, 41550]

    # Create subplots for multiple metrics in a 2x2 grid
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Revenue", "CVR", "AOV", "Gross Profits"))

    # For Revenue
    combined_values_revenue = before_monocle + after_monocle
    combined_projected_revenue = before_monocle + projected_without_monocle
    fig.add_trace(go.Scatter(x=dates, y=combined_values_revenue, mode='lines+markers', name='Revenue (Monocle Impact)', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=combined_projected_revenue, mode='lines+markers', name='Revenue (Projected w/o Monocle)', line=dict(color='red', dash='dot')), row=1, col=1)

    # For CVR
    combined_values_cvr = [0.10, 0.12, 0.11, 0.08, 0.10] + [0.17, 0.19, 0.23, 0.22, 0.24]
    combined_projected_cvr = [0.10, 0.12, 0.11, 0.08, 0.10] + [0.11, 0.10, 0.09, 0.10, 0.12]
    fig.add_trace(go.Scatter(x=dates, y=combined_values_cvr, mode='lines+markers', name='CVR (Monocle Impact)', line=dict(color='green')), row=1, col=2)
    fig.add_trace(go.Scatter(x=dates, y=combined_projected_cvr, mode='lines+markers', name='CVR (Projected w/o Monocle)', line=dict(color='red', dash='dot')), row=1, col=2)

    # For AOV
    combined_values_aov = [400, 450, 470, 490, 500] + [700, 750, 840, 820, 890]
    combined_projected_aov = [400, 450, 470, 490, 500] + [510, 520, 530, 540, 550]
    fig.add_trace(go.Scatter(x=dates, y=combined_values_aov, mode='lines+markers', name='AOV (Monocle Impact)', line=dict(color='green')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=combined_projected_aov, mode='lines+markers', name='AOV (Projected w/o Monocle)', line=dict(color='red', dash='dot')), row=2, col=1)

    # For Gross Profits
    combined_values_gross_profits = [7000, 7200, 7400, 7500, 7700] + [10500, 11300, 10900, 11500, 12400]
    combined_projected_gross_profits = [7000, 7200, 7400, 7500, 7700] + [7800, 7900, 8000, 8100, 8200]
    fig.add_trace(go.Scatter(x=dates, y=combined_values_gross_profits, mode='lines+markers', name = 'Gross Profit (Monocle Impact)', line=dict(color='green')), row=2, col=2)
    fig.add_trace(go.Scatter(x=dates, y=combined_projected_gross_profits, mode='lines+markers',name= 'Gross Profit (Projected w/o Monocle)', line=dict(color='red', dash='dot')), row=2, col=2)

    # Add a single intervention marker for all graphs
    fig.add_trace(go.Scatter(x=[dates[5]], y=[after_monocle[0]], mode='markers+text', marker=dict(color='black', size=12),
                             text=["Intervention"], textposition="bottom center", name="Intervention"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[dates[5]], y=[0.17], mode='markers+text', marker=dict(color='black', size=12),
                             text=["Intervention"], textposition="bottom center", name="Intervention"), row=1, col=2)
      # Add a single intervention marker for all graphs
    fig.add_trace(go.Scatter(x=[dates[5]], y=[700], mode='markers+text', marker=dict(color='black', size=12),
                             text=["Intervention"], textposition="bottom center", name="Intervention"), row=2, col=1)
      # Add a single intervention marker for all graphs
    fig.add_trace(go.Scatter(x=[dates[5]], y=[10500], mode='markers+text', marker=dict(color='black', size=12),
                             text=["Intervention"], textposition="bottom center", name="Intervention"), row=2, col=2)
    
    fig.update_layout(height=800, title_text="Overall Campaign Performance")
    st.plotly_chart(fig)

    # Detailed campaign view section
    st.subheader("Detailed Campaign View")
    campaign_name = st.text_input("Enter Campaign Name (Workspace Name)")
    
    if st.button("Show Detailed Campaign Insights"):
        if campaign_name:
            st.write(f"Detailed insights for campaign: {campaign_name}")
            
            categories = ['CVR', 'ARPU', 'AOV', 'Lift in Revenue', 'Incremental Profits']
            baseline = [10, 20, 30, 5, 7]  # Dummy baseline data
            monocle = [15, 25, 30, 10, 12]  # Dummy monocle data (AOV remains similar)
            
            fig_detailed = go.Figure(data=[
                go.Bar(name='Baseline', x=categories, y=baseline, marker_color='lightskyblue'),
                go.Bar(name='Monocle', x=categories, y=monocle, marker_color='lightcoral')
            ])
            fig_detailed.update_layout(title=f"Performance Metrics for {campaign_name}",
                                       xaxis_title="Metrics",
                                       yaxis_title="Percentage (%)",
                                       barmode='group')
            st.plotly_chart(fig_detailed)
        else:
            st.error("Please enter a valid Campaign Name.")

# Integration Section
elif menu == "Integration":
    st.header("Integration")
    st.write("Here you would add options related to Integration.")

# Users Section
elif menu == "Users":
    st.header("Users")
    st.write("Here you would add options related to Users.")
