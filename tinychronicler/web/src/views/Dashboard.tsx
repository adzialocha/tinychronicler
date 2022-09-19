import React from 'react';
import { Desktop } from 'react95';

const Dashboard: React.FC = () => {
  return (
    <Desktop
      backgroundStyles={{
        background: 'blue',
        alignItems: 'center',
        justifyContent: 'center',
        display: 'flex',
        fontSize: 50,
      }}
    >
      💌
    </Desktop>
  );
};

export default Dashboard;
