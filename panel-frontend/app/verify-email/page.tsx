"use client";
import { useEffect, useState } from "react";

export default function Page({ searchParams }: { searchParams: { token?: string } }) {
  const API = process.env.NEXT_PUBLIC_API_BASE || "";
  const [state, setState] = useState<'idle'|'ok'|'error'>('idle');

  useEffect(() => {
    const token = searchParams?.token;
    if (!token) return setState('error');
    (async () => {
      const res = await fetch(`${API}/api/account/verify-email`, {
        method: 'POST', credentials: 'include', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ token })
      });
      setState(res.ok ? 'ok' : 'error');
    })();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <section style={{padding:20}}>
      <h1>Email Verification</h1>
      {state==='idle' && <p>Verifying...</p>}
      {state==='ok' && <p>Verified! You can now <a href="/auth/login">login</a>.</p>}
      {state==='error' && <p style={{color:'crimson'}}>Invalid or expired verification link.</p>}
    </section>
  );
}
