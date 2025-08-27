import streamlit as st
import time

# Configure page
st.set_page_config(
    page_title="TechShop Pro - Premium Tech Store",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main background gradient */
    .main > div {
        background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 50%, #faf5ff 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Product card styling */
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .product-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .product-price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    
    .product-stock {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .product-category {
        background: #f3f4f6;
        color: #374151;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .low-stock {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Cart item styling */
    .cart-item {
        background: white;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    
    /* Metrics styling */
    .metric-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Summary box styling */
    .summary-box {
        background: linear-gradient(135deg, #8b5cf6, #6d28d9);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    /* Success message */
    .success-msg {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Error message */
    .error-msg {
        background: linear-gradient(90deg, #ef4444, #dc2626);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        border: none;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = {
        "A": {"name": "Mouse", "price": 100, "stock": 10, "category": "Accessories", "emoji": "🖱️"},
        "B": {"name": "Keyboard", "price": 200, "stock": 15, "category": "Accessories", "emoji": "⌨️"},
        "C": {"name": "Monitor", "price": 300, "stock": 8, "category": "Display", "emoji": "🖥️"},
        "D": {"name": "Headphones", "price": 400, "stock": 12, "category": "Audio", "emoji": "🎧"},
        "E": {"name": "USB Cable", "price": 500, "stock": 7, "category": "Accessories", "emoji": "🔌"},
        "F": {"name": "Webcam", "price": 600, "stock": 9, "category": "Camera", "emoji": "📷"},
        "G": {"name": "Printer", "price": 700, "stock": 5, "category": "Office", "emoji": "🖨️"},
        "H": {"name": "Laptop Bag", "price": 800, "stock": 6, "category": "Accessories", "emoji": "🎒"}
    }

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Helper functions
def add_to_cart(product_code, quantity):
    product = st.session_state.products[product_code]
    if quantity <= product["stock"]:
        st.session_state.cart[product_code] = st.session_state.cart.get(product_code, 0) + quantity
        st.session_state.products[product_code]["stock"] -= quantity
        
        # Generate recommendations
        st.session_state.recommendations = [
            code for code in st.session_state.products.keys() 
            if code != product_code
        ][:4]
        
        st.success(f"✅ {quantity} {product['name']}(s) added to cart!")
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ Not enough stock available!")

def remove_from_cart(product_code, quantity):
    if product_code not in st.session_state.cart:
        st.error("❌ Product not found in cart!")
        return
    
    current_qty = st.session_state.cart[product_code]
    if quantity >= current_qty:
        st.session_state.products[product_code]["stock"] += current_qty
        del st.session_state.cart[product_code]
        st.success(f"✅ All {st.session_state.products[product_code]['name']} removed from cart!")
    else:
        st.session_state.cart[product_code] -= quantity
        st.session_state.products[product_code]["stock"] += quantity
        st.success(f"✅ {quantity} {st.session_state.products[product_code]['name']}(s) removed from cart!")
    
    time.sleep(1)
    st.rerun()

def calculate_totals():
    total = sum(
        st.session_state.products[code]["price"] * qty 
        for code, qty in st.session_state.cart.items()
    )
    discount = total * 0.05
    final_amount = total - discount
    return total, discount, final_amount

def get_cart_count():
    return sum(st.session_state.cart.values())

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚀 TechShop Pro</h1>
    <p class="header-subtitle">Premium Tech Store - Your One-Stop Shop for Quality Electronics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    page = st.selectbox(
        "Choose Section:",
        ["🛍️ Browse Products", "🛒 Shopping Cart", "📊 Analytics"],
        key="navigation"
    )
    
    # Cart summary in sidebar
    cart_count = get_cart_count()
    if cart_count > 0:
        st.markdown("### 🛒 Cart Summary")
        total, discount, final = calculate_totals()
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Items: {cart_count}</h4>
            <h4>Total: ₹{final:.2f}</h4>
        </div>
        """, unsafe_allow_html=True)

# Main content area
if page == "🛍️ Browse Products":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🌟 Featured Products")
        st.markdown("*Discover our premium tech collection with exclusive offers*")
    
    with col2:
        if cart_count > 0:
            st.metric("Cart Items", cart_count, delta=None)
    
    # Product grid
    cols = st.columns(4)
    for i, (code, product) in enumerate(st.session_state.products.items()):
        with cols[i % 4]:
            # Stock status
            stock_status = "low-stock" if product["stock"] < 5 else "product-category"
            stock_text = "⚠️ Low Stock" if product["stock"] < 5 else product["category"]
            
            st.markdown(f"""
            <div class="product-card">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">
                    {product["emoji"]}
                </div>
                <div class="{stock_status}">{stock_text}</div>
                <div class="product-name">{product["name"]}</div>
                <div class="product-price">₹{product["price"]}</div>
                <div class="product-stock">Stock: {product["stock"]} units</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quantity selector and add button
            quantity = st.number_input(
                "Quantity", 
                min_value=1, 
                max_value=max(1, product["stock"]), 
                value=1, 
                key=f"qty_{code}"
            )
            
            if st.button(f"Add to Cart", key=f"add_{code}", disabled=product["stock"] == 0):
                add_to_cart(code, quantity)

    # Recommendations
    if st.session_state.recommendations:
        st.markdown("---")
        st.markdown("### 📈 Recommended for You")
        rec_cols = st.columns(4)
        for i, rec_code in enumerate(st.session_state.recommendations):
            with rec_cols[i]:
                rec_product = st.session_state.products[rec_code]
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2rem;">{rec_product["emoji"]}</div>
                    <div style="font-weight: bold; margin: 0.5rem 0;">{rec_product["name"]}</div>
                    <div style="color: #059669; font-weight: bold;">₹{rec_product["price"]}</div>
                </div>
                """, unsafe_allow_html=True)

elif page == "🛒 Shopping Cart":
    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
            <h2 style="color: #6b7280;">Your cart is empty</h2>
            <p style="color: #9ca3af;">Add some products to get started</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🛒 Cart Items")
            
            for code, qty in st.session_state.cart.items():
                product = st.session_state.products[code]
                item_total = product["price"] * qty
                
                st.markdown(f"""
                <div class="cart-item">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="font-size: 2rem;">{product["emoji"]}</div>
                            <div>
                                <div style="font-weight: bold; font-size: 1.1rem;">{product["name"]}</div>
                                <div style="color: #6b7280;">₹{product["price"]} each</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: bold; font-size: 1.2rem; color: #059669;">₹{item_total}</div>
                            <div style="color: #6b7280;">Quantity: {qty}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Remove options
                remove_col1, remove_col2, remove_col3 = st.columns(3)
                with remove_col1:
                    if st.button(f"Remove 1", key=f"remove1_{code}"):
                        remove_from_cart(code, 1)
                with remove_col2:
                    if st.button(f"Remove All", key=f"removeall_{code}"):
                        remove_from_cart(code, qty)
                with remove_col3:
                    add_qty = st.number_input("Add more", min_value=1, max_value=product["stock"], key=f"addmore_{code}")
                    if st.button(f"Add {add_qty}", key=f"addmore_btn_{code}"):
                        add_to_cart(code, add_qty)
        
        with col2:
            total, discount, final = calculate_totals()
            
            st.markdown(f"""
            <div class="summary-box">
                <h3 style="margin-top: 0;">🎁 Order Summary</h3>
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Subtotal:</span>
                        <span>₹{total}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; color: #86efac;">
                        <span>Discount (5%):</span>
                        <span>-₹{discount:.2f}</span>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold;">
                        <span>Final Total:</span>
                        <span>₹{final:.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Checkout Now", key="checkout"):
                st.markdown("""
                <div class="success-msg">
                    🎉 Thank you for shopping! Order placed successfully! 🎉
                </div>
                """, unsafe_allow_html=True)
                st.session_state.cart = {}
                time.sleep(2)
                st.rerun()

elif page == "📊 Analytics":
    st.markdown("### 📊 Store Analytics")
    
    # Store metrics
    total_products = len(st.session_state.products)
    total_stock = sum(p["stock"] for p in st.session_state.products.values())
    low_stock_items = sum(1 for p in st.session_state.products.values() if p["stock"] < 5)
    cart_value = calculate_totals()[2] if st.session_state.cart else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", total_products, delta=None)
    with col2:
        st.metric("Total Stock", total_stock, delta=None)
    with col3:
        st.metric("Low Stock Items", low_stock_items, delta=None)
    with col4:
        st.metric("Cart Value", f"₹{cart_value:.2f}", delta=None)
    
    # Product stock chart
    st.markdown("### 📈 Stock Levels")
    chart_data = {
        "Product": [p["name"] for p in st.session_state.products.values()],
        "Stock": [p["stock"] for p in st.session_state.products.values()],
        "Price": [p["price"] for p in st.session_state.products.values()]
    }
    
    st.bar_chart(data={p["name"]: p["stock"] for p in st.session_state.products.values()})
    
    # Category breakdown
    st.markdown("### 🏷️ Category Breakdown")
    categories = {}
    for product in st.session_state.products.values():
        category = product["category"]
        categories[category] = categories.get(category, 0) + 1
    
    st.bar_chart(categories)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🚀 TechShop Pro - Built with Streamlit | Premium Tech Store Experience</p>
</div>
""", unsafe_allow_html=True)