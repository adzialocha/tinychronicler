const ENDPOINT = '/api';

export const METHOD_GET = 'GET';
export const METHOD_POST = 'POST';
export const METHOD_PUT = 'PUT';
export const METHOD_DELETE = 'DELETE';

function encode(str) {
  return encodeURIComponent(str);
}

function parameterize(obj) {
  if (Object.keys(obj).length === 0) {
    return '';
  }

  return (
    '?' +
    Object.keys(obj)
      .reduce((acc, key) => {
        if (Array.isArray(obj[key])) {
          if (obj[key].length === 0) {
            return acc;
          }

          const merged = obj[key]
            .map((item) => {
              return `${encode(key)}[]=${encode(item)}`;
            })
            .join('&');

          acc.push(merged);
          return acc;
        }

        acc.push(`${encode(key)}=${encode(obj[key])}`);
        return acc;
      }, [])
      .join('&')
  );
}

export default async function request(path = [], body = {}, method = METHOD_GET) {
  const headers = {};
  if (!(body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const options = {
    method,
    headers: new Headers({
      ...headers,
    }),
  };

  // Format the body depending on our request method
  let paramsStr = '';
  if (body) {
    if (options.method === METHOD_GET) {
      paramsStr = parameterize(body);
    } else if (body instanceof FormData) {
      options.body = body;
    } else {
      options.body = JSON.stringify(body);
    }
  }

  const response = await window.fetch(`${ENDPOINT}/${path.join('/')}${paramsStr}`, options);

  const contentType = response.headers.get('Content-Type');
  if (contentType && contentType.includes('application/json')) {
    return await response.json();
  }

  return await response.text();
}
