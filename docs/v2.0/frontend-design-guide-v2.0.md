# **Frontend Design Guide for stackdocs**

## **1. Introduction**

This document guides the development of the stackdocs frontend, emphasizing a sleek, glassmorphic top bar, minimalistic design, and fluid animations inspired by Vercel, Framer, and Linear. The goal is to create an intuitive, visually stunning interface that enhances user engagement and professionalism.

---

## **2. Design Principles**

- **Clarity & Simplicity:** Clear hierarchy, ample whitespace, no clutter.
- **Liquid Glass Aesthetic:** Translucent, frosted glass look with subtle curves and soft shadows.
- **Fluid Animations:** Smooth, natural transitions using Framer Motion.
- **Consistency:** Use unified color schemes, fonts, and motion behaviors.
- **Accessibility:** Focus states, keyboard navigation, and readable contrast.

---

## **3. Color & Style**

### **Primary Palette**

- Frosted white semi-transparent background: `rgba(255,255,255,0.1)`
- Text & icons: Dark gray `#222` | White for contrast
- Accent / Highlight: Soft blue or teal for selections and hover states

### **Glassmorphism Effects**

```css
backdrop-filter: blur(20px);
background: rgba(255, 255, 255, 0.12);
border-radius: 16px;
box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
```

---

## **4. Layout & Components**

### **Top Bar**

- **Position:** Fixed to top, full width
- **Height:** 60-70px
- **Style:** Floating, curved edges, translucent glass with backdrop blur
- **Content:**
  - **Left:** Logo/Brand
  - **Center:** Stack selector (dropdown or button)
  - **Right:** Search, Chat, User avatar/settings

### **Navigation & Interaction**

- **Dropdown menus & buttons:** Rounded corners, semi-transparent background
- **Hover/Focus:** Subtle glow or soft shadow
- **Animations:** Animate opening, closing, hover effects using Framer Motion

---

## **5. Components & UI Elements**

| Element                 | Style & Behavior                                           | Inspiration                |
| ----------------------- | ---------------------------------------------------------- | -------------------------- |
| **Top Bar Container**   | Glassmorphic, curved, shadow, fixed position               | Vercel, Apple Liquid Glass |
| **Buttons**             | Rounded, semi-transparent, hover glow, animated scale      | Linear, Framer             |
| **Dropdowns**           | Rounded, semi-transparent, subtle shadow, animated fade-in | Vercel, Linear UI          |
| **Icons & Inputs**      | Minimal, outlines, mild shadows, smooth focus animations   | Framer, Linear             |
| **Floating Animations** | Subtle floating or bouncing on hover/interaction           | Framer Motion              |

---

## **6. Animations & Motion**

- Use **Framer Motion** for:
  - **Smooth fade-in/out** for menu opening
  - Fluid hover effects (scale, glow)
  - Floating or gentle bouncing to give a floating, liquid feel
- Example:

```jsx
<motion.div
  initial={{ opacity: 0, y: -10 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: "easeInOut" }}
>
  {/* component */}
</motion.div>
```

---

## **7. Accessibility & Usability**

- Focus outlines with glow or soft shadow
- Keyboard navigation with `tabindex`
- ARIA labels for dropdowns and interactive icons
- Sufficient color contrast

---

## **8. Developer Implementation Tips**

- Use **Tailwind CSS** for rapid styling, extended with **custom CSS** for glassmorphism effects
- Structure components for reusability (Button, Navbar, Dropdown, IconButton)
- Use **Framer Motion** hooks or components (`motion.div`, `AnimatePresence`) for fluid animations
- Maintain consistent spacing, with a base grid (8px, 16px)

---

## **Sample Color & Glass CSS**

```css
/* Glassmorphic style class */
.glass-card {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

---

## **9. Visual Style References**

- **Vercel:** Minimal, clean, floating UI cards, transparent navbars
- **Framer:** Fluid, natural animations and transitions
- **Linear:** Focus on simplicity, subtle motion, and style consistency
- **Apple Liquid Glass:** Curved, transparent, floating glass effect

---

## **10. Next Steps**

- Prototype key components in Figma or Figma + Tailwind Templates
- Develop React components with shadcn/ui + Framer Motion
- Iterate on style and animation to match aesthetic goals

---

Would you like me to prepare a sample React component code for the top bar?

Sources

Summary MVP UX checklist
• Drag-and-drop file upload area
• Upload progress spinner with real-time status text (e.g., "Uploading…", "Processing document…", "Generating summary…")
• Automated generation of title and description via Docling + AI summarization agent
• Display generated metadata in document list
• Clear success or error notification once processing completes

---

## **11. Updated Design Direction - iOS 26 Liquid Glass (October 2025)**

### **Design Evolution**

The original design guide referenced traditional glassmorphism. We're now aligning with **Apple's Liquid Glass design language** introduced in iOS 26 (September 2025), which represents the biggest visual change to iOS since iOS 7 in 2013.

### **What is Liquid Glass?**

Liquid Glass is a translucent meta-material that:
- **Reflects and refracts** surroundings like real glass
- **Responds dynamically** to light, motion, and environment in real-time
- **Uses physically accurate lensing** and shaders for realistic rendering
- **Adapts intelligently** between light and dark environments
- **Transforms fluidly** (e.g., tab bars shrink on scroll, expand on scroll-up)

### **Design Lineage**

Liquid Glass combines elements from:
- Mac OS X Aqua (original glass buttons)
- iOS 7 real-time blurs (frosted glass)
- iPhone X gesture fluidity
- Dynamic Island flexibility
- visionOS immersive glass interface

### **Key Implementation Differences**

| Aspect | Static Glassmorphism | Liquid Glass (iOS 26) |
|--------|---------------------|---------------------|
| **Blur** | Fixed blur radius | Dynamic blur responding to scroll/interaction |
| **Color** | Fixed semi-transparent | Adapts to surrounding content colors |
| **Animation** | Simple fade/slide | Fluid transformations with physics-based easing |
| **Highlights** | Static shadow | Specular highlights moving with interaction |
| **Behavior** | Passive background | Active, responsive material |

### **Updated CSS Approach**

**Enhanced glassmorphism with dynamic properties:**

```css
/* Liquid Glass Base Style */
.liquid-glass {
  backdrop-filter: blur(20px) saturate(180%);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.12) 0%,
    rgba(255, 255, 255, 0.08) 100%
  );
  border-radius: 16px;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}

/* Tinted Mode (Better Accessibility) */
.liquid-glass-tinted {
  backdrop-filter: blur(20px) saturate(180%);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.18) 0%,
    rgba(255, 255, 255, 0.12) 100%
  );
  /* Higher opacity for better text contrast */
}
```

### **Framer Motion Integration**

**Liquid behavior animations:**

```jsx
// Physics-based spring animations for organic feel
const liquidVariants = {
  initial: {
    opacity: 0,
    y: -20,
    scale: 0.95
  },
  animate: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24
    }
  },
  hover: {
    scale: 1.02,
    boxShadow: "0 8px 30px rgba(0, 0, 0, 0.12)",
    transition: { duration: 0.2 }
  }
};

// Usage in component
<motion.div
  variants={liquidVariants}
  initial="initial"
  animate="animate"
  whileHover="hover"
  className="liquid-glass"
>
  {/* Content */}
</motion.div>
```

### **Top Bar Dynamic Behavior (iOS 26 Pattern)**

The top bar should respond to scroll:

- **Default state**: Full height (60-70px), standard transparency
- **On scroll down**: Shrinks slightly, increases transparency, content takes focus
- **On scroll up**: Expands back to full size, returns to standard transparency
- **Result**: Content remains primary while keeping navigation accessible

### **Performance Considerations**

Liquid Glass effects can be computationally expensive:

1. **Use sparingly**: Apply `backdrop-filter` to key UI elements only (top bar, modals, cards)
2. **Optimize with `will-change`**: Add `will-change: backdrop-filter` to elements that will animate, but remove after animation completes
3. **Test on lower-end devices**: Ensure frame rates stay above 60fps
4. **Provide fallback**: For browsers without `backdrop-filter` support, use semi-transparent solid backgrounds

### **Accessibility Approach**

iOS 26 received criticism for reduced contrast and text legibility. Our approach:

1. **Start with "Tinted" mode**: Slightly more opaque than full transparency (better contrast)
2. **Ensure sufficient color contrast**: Test all text against glassmorphic backgrounds (WCAG AA minimum)
3. **Focus states**: Clear glow or shadow on interactive elements
4. **Consider toggle**: Allow users to reduce transparency if needed (future enhancement)

### **Color Palette Updates**

```css
/* Light Mode */
:root {
  --glass-bg: rgba(255, 255, 255, 0.08);
  --glass-bg-tinted: rgba(255, 255, 255, 0.18);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-highlight: rgba(255, 255, 255, 0.4);
  --text-primary: #222;
  --accent-blue: #007AFF; /* iOS blue */
}

/* Dark Mode */
:root.dark {
  --glass-bg: rgba(0, 0, 0, 0.3);
  --glass-bg-tinted: rgba(0, 0, 0, 0.45);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-highlight: rgba(255, 255, 255, 0.2);
  --text-primary: #FFF;
}
```

### **References & Inspiration**

- **Apple Newsroom**: [Introducing Liquid Glass Design](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)
- **WWDC 2025**: Session 219 - "Meet Liquid Glass"
- **iOS 26 Design Guidelines**: Apple Human Interface Guidelines (2025 Edition)
- **Critical Analysis**: Nielsen Norman Group - "Liquid Glass Is Cracked, and Usability Suffers in iOS 26"

### **Implementation Priority**

1. **Phase 1 (MVP)**: Basic glassmorphic effects with fixed transparency (tinted mode)
2. **Phase 2**: Add Framer Motion animations for smooth interactions
3. **Phase 3**: Implement dynamic scroll-based top bar behavior
4. **Phase 4 (Polish)**: Add specular highlights and advanced lighting effects

This updated direction ensures Vectory v2.0 feels modern and aligned with 2025 design trends while maintaining usability and performance.
