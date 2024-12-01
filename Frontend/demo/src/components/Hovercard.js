import React from 'react'
import { styled, keyframes } from '@stitches/react';
import { mauve } from '@radix-ui/colors';
import * as HoverCardPrimitive from '@radix-ui/react-hover-card';
import Dialogue from './Dialogue';

const slideUpAndFade = keyframes({
    '0%': { opacity: 0, transform: 'translateY(2px)' },
    '100%': { opacity: 1, transform: 'translateY(0)' },
  });
  
  const slideRightAndFade = keyframes({
    '0%': { opacity: 0, transform: 'translateX(-2px)' },
    '100%': { opacity: 1, transform: 'translateX(0)' },
  });
  
  const slideDownAndFade = keyframes({
    '0%': { opacity: 0, transform: 'translateY(-2px)' },
    '100%': { opacity: 1, transform: 'translateY(0)' },
  });
  
  const slideLeftAndFade = keyframes({
    '0%': { opacity: 0, transform: 'translateX(2px)' },
    '100%': { opacity: 1, transform: 'translateX(0)' },
  });
  
  const StyledContent = styled(HoverCardPrimitive.Content, {
    borderRadius: 6,
    padding: 20,
    width: 300,
    backgroundColor: 'white',
    boxShadow: 'hsl(206 22% 7% / 35%) 0px 10px 38px -10px, hsl(206 22% 7% / 20%) 0px 10px 20px -15px',
    '@media (prefers-reduced-motion: no-preference)': {
      animationDuration: '5000ms',
      animationTimingFunction: 'cubic-bezier(0.16, 1, 0.3, 1)',
      willChange: 'transform, opacity',
      '&[data-state="open"]': {
        '&[data-side="top"]': { animationName: slideDownAndFade },
        '&[data-side="right"]': { animationName: slideLeftAndFade },
        '&[data-side="bottom"]': { animationName: slideUpAndFade },
        '&[data-side="left"]': { animationName: slideRightAndFade },
      },
    },
  });
  
  const StyledArrow = styled(HoverCardPrimitive.Arrow, {
    fill: 'white',
  });
  
  // Exports
  export const HoverCard = HoverCardPrimitive.Root;
  export const HoverCardTrigger = HoverCardPrimitive.Trigger;
  export const HoverCardContent = StyledContent;
  export const HoverCardArrow = StyledArrow;
  
  // Your app...
  const Flex = styled('div', { display: 'flex' });
  
  const ImageTrigger = styled('a', {
    all: 'unset',
    cursor: 'pointer',
    borderRadius: '100%',
    display: 'inline-block',
    '&:focus': { boxShadow: `0 0 0 2px black` },
  });
  
  const Img = styled('img', {
    display: 'block',
    borderRadius: '100%',
    variants: {
      size: {
        normal: { width: 45, height: 45 },
        large: { width: 60, height: 60 },
      },
    },
    defaultVariants: {
      size: 'normal',
    },
  });
  
  const Text = styled('div', {
    margin: 0,
    color: mauve.mauve12,
    fontSize: 15,
    lineHeight: 1.5,
    variants: {
      faded: {
        true: { color: mauve.mauve10 },
      },
      bold: {
        true: { fontWeight: 500 },
      },
    },
  });



function Hovercard() {
    return (
    <HoverCard> 
    <HoverCardTrigger asChild>
      <ImageTrigger>
        <Img src="https://static.thenounproject.com/png/1559154-200.png" />
      </ImageTrigger>
    </HoverCardTrigger>
    <HoverCardContent sideOffset={5}>   
      <Flex css={{ flexDirection: 'column', gap: 7 }}>
        <Img
          size="large"
          src="https://static.thenounproject.com/png/1559154-200.png"
        />
        <Flex css={{ flexDirection: 'column', gap: 15 }}>
          <Text>
            <Text bold>Jane Doe</Text>
            <Text faded>@festo</Text>
          </Text>
          <Text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
          sed do eiusmod tempor incididunt ut labore et dolore 
          magna aliqua. Ut enim ad minim veniam, quis nostrud 
          exercitation ullamco laboris nisi ut aliquip ex ea 
          commodo consequat. Duis aute irure dolor in 
          reprehenderit in voluptate velit esse cillum dolore  
          </Text>
          <Flex css={{ gap: 15 }}>
            <Flex css={{ gap: 5 }}>
              {/* <Text bold>0</Text> <Text faded>Following</Text> */}
            </Flex>
            <Flex css={{ gap: 5 }}>
              {/* <Text bold>2,900</Text> <Text faded>Followers</Text> */}
            </Flex>
          </Flex>
        </Flex>
      </Flex>
      <HoverCardArrow />
    </HoverCardContent>
  </HoverCard>
    )
}

export default Hovercard
