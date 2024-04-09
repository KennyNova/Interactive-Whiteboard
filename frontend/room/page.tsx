
import { Tldraw } from 'tldraw';

export default function Room() {


    return (
    <main>
      <div style={{ position: 'fixed', inset: 0 }}>
        <Tldraw></Tldraw>
      </div>
    </main>
  );
}