export async function fetchDashboard() {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/summary`);
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard data');
  }
  return response.json();
}
