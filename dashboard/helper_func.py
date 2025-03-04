class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_df(self):
        daily_orders_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        }).reset_index()

        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)

        return daily_orders_df

    def create_sum_orders_df(self):
        product_sales = self.df.groupby('product_category_name_english')[
            'order_item_id'].sum().reset_index()
        product_sales = product_sales.sort_values(
            by='order_item_id', ascending=False)

        return product_sales

    def create_monthly_orders_df(self):
        df_copy = self.df.copy()
        df_copy['order_month'] = df_copy['order_purchase_timestamp'].dt.to_period(
            'M')
        monthly_orders = df_copy.groupby('order_month')[
            'order_id'].count().reset_index()
        monthly_orders['order_month'] = monthly_orders['order_month'].astype(
            str)

        return monthly_orders

    def create_sum_revenue_df(self):
        df_copy = self.df.copy()
        df_copy['revenue'] = df_copy['price'] * df_copy['order_item_id']
        product_revenue = df_copy.groupby('product_category_name_english')[
            'revenue'].sum().reset_index()
        total_revenue = product_revenue['revenue'].sum()
        product_revenue['contribution (%)'] = (
            product_revenue['revenue'] / total_revenue) * 100
        product_revenue = product_revenue.sort_values(
            by='revenue', ascending=False)

        return product_revenue

    def create_sum_payments_df(self):
        payment_counts = self.df['payment_type'].value_counts(
            normalize=True).reset_index()
        payment_counts.columns = ['payment_type', 'percentage']

        return payment_counts

    def create_sum_by_state_df(self):
        by_state = self.df.groupby(by="customer_state")[
            "customer_id"].nunique().reset_index()
        by_state.rename(
            columns={"customer_id": "customer_count"}, inplace=True)
        by_state = by_state.sort_values(by="customer_count", ascending=False)

        return by_state

    def create_rfm_df(self):
        reference_date = self.df['order_purchase_timestamp'].max()

        rfm = self.df.groupby('customer_id').agg({
            'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
            'order_id': 'nunique',
            'payment_value': 'sum'
        })

        rfm.columns = ['Recency', 'Frequency', 'Monetary']

        return rfm


class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        # Mengunduh gambar peta Brasil dari URL
        image_url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
        with self.urllib.request.urlopen(image_url) as response:
            brazil = self.mpimg.imread(response, format='jpg')

        # Membuat figure dan axis baru (thread-safe)
        fig, ax = self.plt.subplots(figsize=(10, 10))

        # Scatter plot titik koordinat
        self.data.plot(
            kind="scatter",
            x="geolocation_lng",
            y="geolocation_lat",
            alpha=0.3,
            s=0.3,
            c='blue',
            ax=ax  # Gunakan axis yang sudah dibuat
        )

        # Menghapus axis dan menampilkan gambar peta
        ax.set_axis_off()
        ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])

        # Menampilkan plot di Streamlit dengan figure yang benar
        self.st.pyplot(fig)
