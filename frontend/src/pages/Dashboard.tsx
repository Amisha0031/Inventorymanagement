import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";
import { fetchDashboard } from "@/services/api";

const COLORS = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444"]; // primary palette

export default function Dashboard() {
  const { data, isLoading, isError } = useQuery(["dashboard"], fetchDashboard);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="animate-spin w-8 h-8 text-primary" />
      </div>
    );
  }

  if (isError || !data) {
    return <div className="text-center text-red-500">Failed to load dashboard.</div>;
  }

  const {
    total_products,
    total_customers,
    total_orders,
    low_stock_products,
    revenue,
    recent_orders,
    orders_per_day,
    inventory_distribution,
    category_breakdown,
  } = data;

  return (
    <div className="space-y-6">
      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
          <CardHeader>
            <CardTitle>Total Products</CardTitle>
          </CardHeader>
          <CardContent className="text-2xl font-bold">{total_products}</CardContent>
        </Card>
        <Card className="bg-gradient-to-r from-emerald-600 to-green-600 text-white">
          <CardHeader><CardTitle>Total Customers</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">{total_customers}</CardContent>
        </Card>
        <Card className="bg-gradient-to-r from-rose-600 to-pink-600 text-white">
          <CardHeader><CardTitle>Total Orders</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">{total_orders}</CardContent>
        </Card>
        <Card className="bg-gradient-to-r from-amber-600 to-yellow-600 text-white">
          <CardHeader><CardTitle>Revenue</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">${revenue.toFixed(2)}</CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Orders per Day */}
        <Card>
          <CardHeader><CardTitle>Orders Per Day (Last 30d)</CardTitle></CardHeader>
          <CardContent className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={orders_per_day}>
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        {/* Inventory Distribution */}
        <Card>
          <CardHeader><CardTitle>Inventory Distribution</CardTitle></CardHeader>
          <CardContent className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={inventory_distribution} dataKey="quantity" nameKey="product_name" cx="50%" cy="50%" outerRadius={80} label>
                  {inventory_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Orders Table */}
      <Card>
        <CardHeader><CardTitle>Recent Orders</CardTitle></CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full table-auto">
              <thead className="bg-gray-100 dark:bg-gray-800">
                <tr>
                  <th className="p-2 text-left">#</th>
                  <th className="p-2 text-left">Customer</th>
                  <th className="p-2 text-left">Date</th>
                  <th className="p-2 text-left">Total</th>
                  <th className="p-2 text-left">Status</th>
                </tr>
              </thead>
              <tbody>
                {recent_orders.map((o) => (
                  <tr key={o.id} className="border-b">
                    <td className="p-2">{o.order_number}</td>
                    <td className="p-2">{o.customer_name}</td>
                    <td className="p-2">{new Date(o.order_date).toLocaleDateString()}</td>
                    <td className="p-2">${o.total_amount.toFixed(2)}</td>
                    <td className="p-2 capitalize">{o.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
