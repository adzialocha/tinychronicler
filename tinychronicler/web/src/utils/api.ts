const ENDPOINT = '/api';

export const METHOD_GET = 'GET';
export const METHOD_POST = 'POST';
export const METHOD_PUT = 'PUT';
export const METHOD_DELETE = 'DELETE';

function encode(str: string): string {
  return encodeURIComponent(str);
}

function parameterize(obj: {
  [key: string]: string | number | string[] | number[];
}): string {
  if (Object.keys(obj).length === 0) {
    return '';
  }

  return (
    '?' +
    Object.keys(obj)
      .reduce<string[]>((acc, key) => {
        const value = obj[key];

        if (Array.isArray(value)) {
          if (value.length === 0) {
            return acc;
          }

          const merged = value
            .map((item) => {
              return `${encode(key)}[]=${encode(item.toString())}`;
            })
            .join('&');

          acc.push(merged);
          return acc;
        }

        acc.push(`${encode(key)}=${encode(value.toString())}`);
        return acc;
      }, [])
      .join('&')
  );
}

export default async function request(
  path: [string?] = [],
  body = {},
  method = METHOD_GET,
) {
  const headers: HeadersInit = {};
  if (!(body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const options: RequestInit = {
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

  const response = await window.fetch(
    `${ENDPOINT}/${path.join('/')}${paramsStr}`,
    options,
  );

  const contentType = response.headers.get('Content-Type');
  let responseBody;
  if (contentType && contentType.includes('application/json')) {
    responseBody = await response.json();
  } else {
    responseBody = await response.text();
  }

  if (response.status >= 400) {
    throw Error(responseBody);
  } else {
    return responseBody;
  }
}
