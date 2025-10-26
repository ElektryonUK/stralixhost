export default function Page() {
  return (
    <section style={{padding:20}}>
      <h1>Control Panel</h1>
      <p>This will become the authenticated panel shell. For now it links to the panel backend endpoints.</p>
      <ul>
        <li><a href="/api/panel/websites/provision">Provision website (stub)</a></li>
        <li><a href="/api/panel/nodes">List nodes (stub)</a></li>
      </ul>
    </section>
  );
}
