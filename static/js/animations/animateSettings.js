const home = gsap.timeline({ defaults: {duration: 1 }});

home
    .from('.left', {x: '-200%', ease: 'power2.out', duration: 0.5})
    .from('.right', {x: '200%', ease: 'power2.out', duration: 0.5})
