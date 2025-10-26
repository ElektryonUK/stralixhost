"use client";
import { useState } from "react";

export default function Page({ searchParams }: { searchParams: { token?: string } }) {
  const API = process.env.NEXT_PUBLIC_API_BASE || "";
  const [password, setPassword] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const token = searchParams?.token;
    if (!token) return setError('Missing reset token');
    const res = await fetch(`${API}/api/account/reset-password`, {
      method: 'POST', credentials: 'include', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ token, new_password: password })
    });
    if (res.ok) setDone(true);
    else {
      const data = await res.json().catch(()=>({}));
      setError(data.detail || 'Reset failed');
    }
  };

  return (
    <section style={{padding:20, maxWidth:480}}>
      <h1>Reset Password</h1>
      {done ? (
        <p>Password reset. You can now <a href="/auth/login">login</a>.</p>
      ) : (
        <form onSubmit={onSubmit} style={{display:'grid', gap:12}}>
          <input placeholder="New password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
          {error && <p style={{color:'crimson'}}>{error}</p>}
          <button type="submit">Set new password</button>
        </form>
      )}
    </section>
  );
}
