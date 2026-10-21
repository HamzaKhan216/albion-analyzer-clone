import os

os.makedirs('/root/albion-analyzer-clone/frontend', exist_ok=True)

frontend_code = """import React, { useState, useEffect } from 'react';

export default function MarketDashboard() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/scanner/listings')
      .then(res => res.json())
      .then(data => setListings(data.listings))
      .catch(err => console.error("Failed to fetch market data", err));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Albion Market Live Feed</h1>
      <table className="min-w-full bg-white shadow-md rounded">
        <thead>
          <tr className="bg-gray-200">
            <th className="py-2 px-4 border-b">Item ID</th>
            <th className="py-2 px-4 border-b">City</th>
            <th className="py-2 px-4 border-b">Price</th>
            <th className="py-2 px-4 border-b">Amount</th>
          </tr>
        </thead>
        <tbody>
          {listings.map((item, index) => (
            <tr key={index} className="text-center">
              <td className="py-2 px-4 border-b">{item.item_id}</td>
              <td className="py-2 px-4 border-b">{item.city}</td>
              <td className="py-2 px-4 border-b">{item.price} silver</td>
              <td className="py-2 px-4 border-b">{item.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
"""

with open('/root/albion-analyzer-clone/frontend/page.tsx', 'w') as f:
    f.write(frontend_code)

print("Frontend dashboard page generated successfully.")
