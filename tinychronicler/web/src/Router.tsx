import { Routes, Route } from 'react-router-dom';

import Chronicles from '~/views/Chronicles';
import Dashboard from '~/views/Dashboard';

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/chronicles" element={<Chronicles />} />
    </Routes>
  );
};

export default Router;
