"use client";
import { useState } from "react";

export default function Page() {
  const API = process.env.NEXT_PUBLIC_API_BASE || "";
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`${API}/api/account/forgot-password`, {
      method: 'POST', credentials: 'include', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email })
    });
    const data = await res.json().catch(()=>({}));
    setMessage(data.message || 'If the email exists, a reset link has been sent.');
  };

  return (
    <section style={{padding:20, maxWidth:480}}>
      <h1>Forgot Password</h1>
      <form onSubmit={onSubmit} style={{display:'grid', gap:12}}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <button type="submit">Send reset link</button>
      </form>
      {message && <p style={{color:'green'}}>{message}</p>}
    </section>
  );
}
