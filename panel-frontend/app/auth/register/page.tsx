"use client";
import { useState } from "react";

export default function Page() {
  const API = process.env.NEXT_PUBLIC_API_BASE || "";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null); setMessage(null);
    const res = await fetch(`${API}/api/auth/register`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, first_name: firstName || undefined, last_name: lastName || undefined })
    });
    const data = await res.json().catch(()=>({}));
    if (res.ok) setMessage(data.message || 'Registered. Please check your email to verify.');
    else setError(data.detail || 'Registration failed');
  };

  return (
    <section style={{padding:20, maxWidth:480}}>
      <h1>Register</h1>
      <form onSubmit={onSubmit} style={{display:'grid', gap:12}}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
        <input placeholder="First name (optional)" value={firstName} onChange={e=>setFirstName(e.target.value)} />
        <input placeholder="Last name (optional)" value={lastName} onChange={e=>setLastName(e.target.value)} />
        {error && <p style={{color:'crimson'}}>{error}</p>}
        {message && <p style={{color:'green'}}>{message}</p>}
        <button type="submit">Create account</button>
      </form>
    </section>
  );
}
