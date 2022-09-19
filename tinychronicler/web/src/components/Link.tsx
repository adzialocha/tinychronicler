import React from 'react';
import { Button } from 'react95';
import { useHref, useLinkClickHandler, useMatch } from 'react-router-dom';

const LinkTo = React.forwardRef(
  (
    {
      to,
      children,
      ...rest
    }: { to: string; children: React.ReactNode } & typeof Button,
    ref,
  ) => {
    const href = useHref(to);
    const match = useMatch(to);
    const handleClick = useLinkClickHandler(to, {});

    return (
      <Button
        {...rest}
        active={match !== null}
        href={href}
        onClick={(event: React.MouseEvent<HTMLAnchorElement>) => {
          handleClick(event);
        }}
        ref={ref}
      >
        {children}
      </Button>
    );
  },
);

const LinkOnClick = React.forwardRef(
  (
    {
      children,
      onClick,
      ...rest
    }: { to: string; children: React.ReactNode } & typeof Button,
    ref,
  ) => {
    return (
      <Button
        {...rest}
        onClick={(event: React.MouseEvent<HTMLAnchorElement>) => {
          onClick(event);
        }}
        ref={ref}
      >
        {children}
      </Button>
    );
  },
);

const Link = React.forwardRef(
  (
    {
      to,
      children,
      onClick,
      ...rest
    }: { to: string; children: React.ReactNode } & typeof Button,
    ref,
  ) => {
    return to ? (
      <LinkTo to={to} {...rest} ref={ref}>
        {children}
      </LinkTo>
    ) : (
      <LinkOnClick onClick={onClick} {...rest} ref={ref}>
        {children}
      </LinkOnClick>
    );
  },
);

export default Link;
