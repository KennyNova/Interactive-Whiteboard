import { useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil';
import { Move } from '@/types/global';

import { DEFAULT_ROOM, roomAtom } from './room.atom';

const COLORS = [
  { name: 'PURPLE', value: '#6B32F3' },
  { name: 'BLUE', value: '#408FF8' },
  { name: 'RED', value: '#F32D27' },
  { name: 'GREEN', value: '#6FCB12' },
  { name: 'GOLD', value: '#A89D6C' },
  { name: 'PINK', value: '#EB29DA' },
  { name: 'MINT', value: '#19CB87' },
  { name: 'RED_LIGHT', value: '#ED7878' },
  { name: 'CYAN', value: '#02CBF6' },
  { name: 'RED_DARK', value: '#BA1555' },
  { name: 'ORANGE', value: '#FF7300' },
];

export const getNextColor = (color?: string) => {
  const index = COLORS.findIndex((colorArr) => colorArr.value === color);

  if (index === -1) return COLORS[0];

  return COLORS[(index + 1) % COLORS.length];
};


export const useRoom = () => {
  const room = useRecoilValue(roomAtom);

  return room;
};

export const useSetRoom = () => {
  const setRoom = useSetRecoilState(roomAtom);

  return setRoom;
};

export const useSetRoomId = () => {
  const setRoomId = useSetRecoilState(roomAtom);

  const handleSetRoomId = (id: string) => {
    setRoomId({ ...DEFAULT_ROOM, id });
  };

  return handleSetRoomId;
};

export const useSetUsers = () => {
  const setRoom = useSetRecoilState(roomAtom);

  const handleAddUser = (userId: string, name: string) => {
    setRoom((prev: { users: any; usersMoves: any; }) => {
      const newUsers = prev.users;
      const newUsersMoves = prev.usersMoves;

      const color = getNextColor([...newUsers.values()].pop()?.color);

      newUsers.set(userId, {
        name,
        color,
      });
      newUsersMoves.set(userId, []);

      return { ...prev, users: newUsers, usersMoves: newUsersMoves };
    });
  };

  const handleRemoveUser = (userId: string) => {
    setRoom((prev: { users: any; usersMoves: any; movesWithoutUser: any; }) => {
      const newUsers = prev.users;
      const newUsersMoves = prev.usersMoves;

      const userMoves = newUsersMoves.get(userId);

      newUsers.delete(userId);
      newUsersMoves.delete(userId);
      return {
        ...prev,
        users: newUsers,
        usersMoves: newUsersMoves,
        movesWithoutUser: [...prev.movesWithoutUser, ...(userMoves || [])],
      };
    });
  };

  const handleAddMoveToUser = (userId: string, moves: Move) => {
    setRoom((prev: { usersMoves: {
      set(userId: string, arg1: any[]): unknown; get: (arg0: string) => any; 
}; }) => {
      const newUsersMoves = prev.usersMoves;
      const oldMoves = prev.usersMoves.get(userId);

      newUsersMoves.set(userId, [...(oldMoves || []), moves]);
      return { ...prev, usersMoves: newUsersMoves };
    });
  };

  const handleRemoveMoveFromUser = (userId: string) => {
    setRoom((prev: { usersMoves: {
      set(userId: string, arg1: any): unknown; get: (arg0: string) => any; 
}; }) => {
      const newUsersMoves = prev.usersMoves;
      const oldMoves = prev.usersMoves.get(userId);
      oldMoves?.pop();

      newUsersMoves.set(userId, oldMoves || []);
      return { ...prev, usersMoves: newUsersMoves };
    });
  };

  return {
    handleAddUser,
    handleRemoveUser,
    handleAddMoveToUser,
    handleRemoveMoveFromUser,
  };
};

export const useMyMoves = () => {
  const [room, setRoom] = useRecoilState(roomAtom);

  const handleAddMyMove = (move: Move) => {
    setRoom((prev: { myMoves: string | any[]; }) => {
      if ((prev.myMoves as any[])[prev.myMoves.length - 1]?.options.mode === 'select')
        return {
          ...prev,
          myMoves: [...(prev.myMoves as any[]).slice(0, prev.myMoves.length - 1), move],
        };

      return { ...prev, myMoves: [...(prev.myMoves as any[]), move] };
    });
  };

  const handleRemoveMyMove = () => {
    const newMoves = [...room.myMoves];
    const move = newMoves.pop();

    setRoom((prev: any) => ({ ...prev, myMoves: newMoves }));

    return move;
  };

  return { handleAddMyMove, handleRemoveMyMove, myMoves: room.myMoves };
};
