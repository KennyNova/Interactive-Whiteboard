
import { NextPage } from 'next';
import { Tldraw } from 'tldraw';

const RoomPage: NextPage = () => { 


    return (
    <main>
      <div style={{ position: 'fixed', inset: 0 }}>
        <Tldraw></Tldraw>
      </div>
    </main>
  );
}