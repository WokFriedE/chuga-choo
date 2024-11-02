import {

	writable
} from 'svelte/store';

export let store_val = writable({});

// store_val.subscribe(value => {
//     console.log(value);
// });