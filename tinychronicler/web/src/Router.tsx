import { Routes, Route } from 'react-router-dom';

import Chronicles from '~/views/Chronicles';
import ChroniclesNew from '~/views/ChroniclesNew';
import Dashboard from '~/views/Dashboard';

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/chronicles" element={<Chronicles />} />
      <Route path="/chronicles/new" element={<ChroniclesNew />} />
    </Routes>
  );
};

export default Router;
