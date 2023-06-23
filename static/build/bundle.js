
(function(l, r) { if (!l || l.getElementById('livereloadscript')) return; r = l.createElement('script'); r.async = 1; r.src = '//' + (self.location.host || 'localhost').split(':')[0] + ':35730/livereload.js?snipver=1'; r.id = 'livereloadscript'; l.getElementsByTagName('head')[0].appendChild(r) })(self.document);
var app = (function (exports) {
    'use strict';

    function noop() { }
    function add_location(element, file, line, column, char) {
        element.__svelte_meta = {
            loc: { file, line, column, char }
        };
    }
    function run(fn) {
        return fn();
    }
    function blank_object() {
        return Object.create(null);
    }
    function run_all(fns) {
        fns.forEach(run);
    }
    function is_function(thing) {
        return typeof thing === 'function';
    }
    function safe_not_equal(a, b) {
        return a != a ? b == b : a !== b || ((a && typeof a === 'object') || typeof a === 'function');
    }
    function is_empty(obj) {
        return Object.keys(obj).length === 0;
    }

    const globals = (typeof window !== 'undefined'
        ? window
        : typeof globalThis !== 'undefined'
            ? globalThis
            : global);
    function append(target, node) {
        target.appendChild(node);
    }
    function insert(target, node, anchor) {
        target.insertBefore(node, anchor || null);
    }
    function detach(node) {
        if (node.parentNode) {
            node.parentNode.removeChild(node);
        }
    }
    function destroy_each(iterations, detaching) {
        for (let i = 0; i < iterations.length; i += 1) {
            if (iterations[i])
                iterations[i].d(detaching);
        }
    }
    function element(name) {
        return document.createElement(name);
    }
    function text(data) {
        return document.createTextNode(data);
    }
    function space() {
        return text(' ');
    }
    function empty() {
        return text('');
    }
    function listen(node, event, handler, options) {
        node.addEventListener(event, handler, options);
        return () => node.removeEventListener(event, handler, options);
    }
    function attr(node, attribute, value) {
        if (value == null)
            node.removeAttribute(attribute);
        else if (node.getAttribute(attribute) !== value)
            node.setAttribute(attribute, value);
    }
    function to_number(value) {
        return value === '' ? null : +value;
    }
    function children(element) {
        return Array.from(element.childNodes);
    }
    function set_input_value(input, value) {
        input.value = value == null ? '' : value;
    }
    function set_style(node, key, value, important) {
        if (value == null) {
            node.style.removeProperty(key);
        }
        else {
            node.style.setProperty(key, value, important ? 'important' : '');
        }
    }
    function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
        const e = document.createEvent('CustomEvent');
        e.initCustomEvent(type, bubbles, cancelable, detail);
        return e;
    }

    let current_component;
    function set_current_component(component) {
        current_component = component;
    }
    function get_current_component() {
        if (!current_component)
            throw new Error('Function called outside component initialization');
        return current_component;
    }
    /**
     * The `onMount` function schedules a callback to run as soon as the component has been mounted to the DOM.
     * It must be called during the component's initialisation (but doesn't need to live *inside* the component;
     * it can be called from an external module).
     *
     * `onMount` does not run inside a [server-side component](/docs#run-time-server-side-component-api).
     *
     * https://svelte.dev/docs#run-time-svelte-onmount
     */
    function onMount(fn) {
        get_current_component().$$.on_mount.push(fn);
    }

    const dirty_components = [];
    const binding_callbacks = [];
    let render_callbacks = [];
    const flush_callbacks = [];
    const resolved_promise = /* @__PURE__ */ Promise.resolve();
    let update_scheduled = false;
    function schedule_update() {
        if (!update_scheduled) {
            update_scheduled = true;
            resolved_promise.then(flush);
        }
    }
    function add_render_callback(fn) {
        render_callbacks.push(fn);
    }
    // flush() calls callbacks in this order:
    // 1. All beforeUpdate callbacks, in order: parents before children
    // 2. All bind:this callbacks, in reverse order: children before parents.
    // 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
    //    for afterUpdates called during the initial onMount, which are called in
    //    reverse order: children before parents.
    // Since callbacks might update component values, which could trigger another
    // call to flush(), the following steps guard against this:
    // 1. During beforeUpdate, any updated components will be added to the
    //    dirty_components array and will cause a reentrant call to flush(). Because
    //    the flush index is kept outside the function, the reentrant call will pick
    //    up where the earlier call left off and go through all dirty components. The
    //    current_component value is saved and restored so that the reentrant call will
    //    not interfere with the "parent" flush() call.
    // 2. bind:this callbacks cannot trigger new flush() calls.
    // 3. During afterUpdate, any updated components will NOT have their afterUpdate
    //    callback called a second time; the seen_callbacks set, outside the flush()
    //    function, guarantees this behavior.
    const seen_callbacks = new Set();
    let flushidx = 0; // Do *not* move this inside the flush() function
    function flush() {
        // Do not reenter flush while dirty components are updated, as this can
        // result in an infinite loop. Instead, let the inner flush handle it.
        // Reentrancy is ok afterwards for bindings etc.
        if (flushidx !== 0) {
            return;
        }
        const saved_component = current_component;
        do {
            // first, call beforeUpdate functions
            // and update components
            try {
                while (flushidx < dirty_components.length) {
                    const component = dirty_components[flushidx];
                    flushidx++;
                    set_current_component(component);
                    update(component.$$);
                }
            }
            catch (e) {
                // reset dirty state to not end up in a deadlocked state and then rethrow
                dirty_components.length = 0;
                flushidx = 0;
                throw e;
            }
            set_current_component(null);
            dirty_components.length = 0;
            flushidx = 0;
            while (binding_callbacks.length)
                binding_callbacks.pop()();
            // then, once components are updated, call
            // afterUpdate functions. This may cause
            // subsequent updates...
            for (let i = 0; i < render_callbacks.length; i += 1) {
                const callback = render_callbacks[i];
                if (!seen_callbacks.has(callback)) {
                    // ...so guard against infinite loops
                    seen_callbacks.add(callback);
                    callback();
                }
            }
            render_callbacks.length = 0;
        } while (dirty_components.length);
        while (flush_callbacks.length) {
            flush_callbacks.pop()();
        }
        update_scheduled = false;
        seen_callbacks.clear();
        set_current_component(saved_component);
    }
    function update($$) {
        if ($$.fragment !== null) {
            $$.update();
            run_all($$.before_update);
            const dirty = $$.dirty;
            $$.dirty = [-1];
            $$.fragment && $$.fragment.p($$.ctx, dirty);
            $$.after_update.forEach(add_render_callback);
        }
    }
    /**
     * Useful for example to execute remaining `afterUpdate` callbacks before executing `destroy`.
     */
    function flush_render_callbacks(fns) {
        const filtered = [];
        const targets = [];
        render_callbacks.forEach((c) => fns.indexOf(c) === -1 ? filtered.push(c) : targets.push(c));
        targets.forEach((c) => c());
        render_callbacks = filtered;
    }
    const outroing = new Set();
    function transition_in(block, local) {
        if (block && block.i) {
            outroing.delete(block);
            block.i(local);
        }
    }

    function destroy_block(block, lookup) {
        block.d(1);
        lookup.delete(block.key);
    }
    function update_keyed_each(old_blocks, dirty, get_key, dynamic, ctx, list, lookup, node, destroy, create_each_block, next, get_context) {
        let o = old_blocks.length;
        let n = list.length;
        let i = o;
        const old_indexes = {};
        while (i--)
            old_indexes[old_blocks[i].key] = i;
        const new_blocks = [];
        const new_lookup = new Map();
        const deltas = new Map();
        const updates = [];
        i = n;
        while (i--) {
            const child_ctx = get_context(ctx, list, i);
            const key = get_key(child_ctx);
            let block = lookup.get(key);
            if (!block) {
                block = create_each_block(key, child_ctx);
                block.c();
            }
            else if (dynamic) {
                // defer updates until all the DOM shuffling is done
                updates.push(() => block.p(child_ctx, dirty));
            }
            new_lookup.set(key, new_blocks[i] = block);
            if (key in old_indexes)
                deltas.set(key, Math.abs(i - old_indexes[key]));
        }
        const will_move = new Set();
        const did_move = new Set();
        function insert(block) {
            transition_in(block, 1);
            block.m(node, next);
            lookup.set(block.key, block);
            next = block.first;
            n--;
        }
        while (o && n) {
            const new_block = new_blocks[n - 1];
            const old_block = old_blocks[o - 1];
            const new_key = new_block.key;
            const old_key = old_block.key;
            if (new_block === old_block) {
                // do nothing
                next = new_block.first;
                o--;
                n--;
            }
            else if (!new_lookup.has(old_key)) {
                // remove old block
                destroy(old_block, lookup);
                o--;
            }
            else if (!lookup.has(new_key) || will_move.has(new_key)) {
                insert(new_block);
            }
            else if (did_move.has(old_key)) {
                o--;
            }
            else if (deltas.get(new_key) > deltas.get(old_key)) {
                did_move.add(new_key);
                insert(new_block);
            }
            else {
                will_move.add(old_key);
                o--;
            }
        }
        while (o--) {
            const old_block = old_blocks[o];
            if (!new_lookup.has(old_block.key))
                destroy(old_block, lookup);
        }
        while (n)
            insert(new_blocks[n - 1]);
        run_all(updates);
        return new_blocks;
    }
    function validate_each_keys(ctx, list, get_context, get_key) {
        const keys = new Set();
        for (let i = 0; i < list.length; i++) {
            const key = get_key(get_context(ctx, list, i));
            if (keys.has(key)) {
                throw new Error('Cannot have duplicate keys in a keyed each');
            }
            keys.add(key);
        }
    }
    function mount_component(component, target, anchor, customElement) {
        const { fragment, after_update } = component.$$;
        fragment && fragment.m(target, anchor);
        if (!customElement) {
            // onMount happens before the initial afterUpdate
            add_render_callback(() => {
                const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
                // if the component was destroyed immediately
                // it will update the `$$.on_destroy` reference to `null`.
                // the destructured on_destroy may still reference to the old array
                if (component.$$.on_destroy) {
                    component.$$.on_destroy.push(...new_on_destroy);
                }
                else {
                    // Edge case - component was destroyed immediately,
                    // most likely as a result of a binding initialising
                    run_all(new_on_destroy);
                }
                component.$$.on_mount = [];
            });
        }
        after_update.forEach(add_render_callback);
    }
    function destroy_component(component, detaching) {
        const $$ = component.$$;
        if ($$.fragment !== null) {
            flush_render_callbacks($$.after_update);
            run_all($$.on_destroy);
            $$.fragment && $$.fragment.d(detaching);
            // TODO null out other refs, including component.$$ (but need to
            // preserve final state?)
            $$.on_destroy = $$.fragment = null;
            $$.ctx = [];
        }
    }
    function make_dirty(component, i) {
        if (component.$$.dirty[0] === -1) {
            dirty_components.push(component);
            schedule_update();
            component.$$.dirty.fill(0);
        }
        component.$$.dirty[(i / 31) | 0] |= (1 << (i % 31));
    }
    function init(component, options, instance, create_fragment, not_equal, props, append_styles, dirty = [-1]) {
        const parent_component = current_component;
        set_current_component(component);
        const $$ = component.$$ = {
            fragment: null,
            ctx: [],
            // state
            props,
            update: noop,
            not_equal,
            bound: blank_object(),
            // lifecycle
            on_mount: [],
            on_destroy: [],
            on_disconnect: [],
            before_update: [],
            after_update: [],
            context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
            // everything else
            callbacks: blank_object(),
            dirty,
            skip_bound: false,
            root: options.target || parent_component.$$.root
        };
        append_styles && append_styles($$.root);
        let ready = false;
        $$.ctx = instance
            ? instance(component, options.props || {}, (i, ret, ...rest) => {
                const value = rest.length ? rest[0] : ret;
                if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
                    if (!$$.skip_bound && $$.bound[i])
                        $$.bound[i](value);
                    if (ready)
                        make_dirty(component, i);
                }
                return ret;
            })
            : [];
        $$.update();
        ready = true;
        run_all($$.before_update);
        // `false` as a special case of no DOM component
        $$.fragment = create_fragment ? create_fragment($$.ctx) : false;
        if (options.target) {
            if (options.hydrate) {
                const nodes = children(options.target);
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.l(nodes);
                nodes.forEach(detach);
            }
            else {
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.c();
            }
            if (options.intro)
                transition_in(component.$$.fragment);
            mount_component(component, options.target, options.anchor, options.customElement);
            flush();
        }
        set_current_component(parent_component);
    }
    /**
     * Base class for Svelte components. Used when dev=false.
     */
    class SvelteComponent {
        $destroy() {
            destroy_component(this, 1);
            this.$destroy = noop;
        }
        $on(type, callback) {
            if (!is_function(callback)) {
                return noop;
            }
            const callbacks = (this.$$.callbacks[type] || (this.$$.callbacks[type] = []));
            callbacks.push(callback);
            return () => {
                const index = callbacks.indexOf(callback);
                if (index !== -1)
                    callbacks.splice(index, 1);
            };
        }
        $set($$props) {
            if (this.$$set && !is_empty($$props)) {
                this.$$.skip_bound = true;
                this.$$set($$props);
                this.$$.skip_bound = false;
            }
        }
    }

    function dispatch_dev(type, detail) {
        document.dispatchEvent(custom_event(type, Object.assign({ version: '3.59.2' }, detail), { bubbles: true }));
    }
    function append_dev(target, node) {
        dispatch_dev('SvelteDOMInsert', { target, node });
        append(target, node);
    }
    function insert_dev(target, node, anchor) {
        dispatch_dev('SvelteDOMInsert', { target, node, anchor });
        insert(target, node, anchor);
    }
    function detach_dev(node) {
        dispatch_dev('SvelteDOMRemove', { node });
        detach(node);
    }
    function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation, has_stop_immediate_propagation) {
        const modifiers = options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
        if (has_prevent_default)
            modifiers.push('preventDefault');
        if (has_stop_propagation)
            modifiers.push('stopPropagation');
        if (has_stop_immediate_propagation)
            modifiers.push('stopImmediatePropagation');
        dispatch_dev('SvelteDOMAddEventListener', { node, event, handler, modifiers });
        const dispose = listen(node, event, handler, options);
        return () => {
            dispatch_dev('SvelteDOMRemoveEventListener', { node, event, handler, modifiers });
            dispose();
        };
    }
    function attr_dev(node, attribute, value) {
        attr(node, attribute, value);
        if (value == null)
            dispatch_dev('SvelteDOMRemoveAttribute', { node, attribute });
        else
            dispatch_dev('SvelteDOMSetAttribute', { node, attribute, value });
    }
    function set_data_dev(text, data) {
        data = '' + data;
        if (text.data === data)
            return;
        dispatch_dev('SvelteDOMSetData', { node: text, data });
        text.data = data;
    }
    function validate_each_argument(arg) {
        if (typeof arg !== 'string' && !(arg && typeof arg === 'object' && 'length' in arg)) {
            let msg = '{#each} only iterates over array-like objects.';
            if (typeof Symbol === 'function' && arg && Symbol.iterator in arg) {
                msg += ' You can use a spread to convert this iterable into an array.';
            }
            throw new Error(msg);
        }
    }
    function validate_slots(name, slot, keys) {
        for (const slot_key of Object.keys(slot)) {
            if (!~keys.indexOf(slot_key)) {
                console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
            }
        }
    }
    /**
     * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
     */
    class SvelteComponentDev extends SvelteComponent {
        constructor(options) {
            if (!options || (!options.target && !options.$$inline)) {
                throw new Error("'target' is a required option");
            }
            super();
        }
        $destroy() {
            super.$destroy();
            this.$destroy = () => {
                console.warn('Component was already destroyed'); // eslint-disable-line no-console
            };
        }
        $capture_state() { }
        $inject_state() { }
    }

    /* src/Table.svelte generated by Svelte v3.59.2 */
    const file$1 = "src/Table.svelte";

    function get_each_context$1(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[10] = list[i];
    	return child_ctx;
    }

    // (67:4) {#each students as student (student.id)}
    function create_each_block$1(key_1, ctx) {
    	let tr;
    	let td0;
    	let t0_value = /*student*/ ctx[10].id + "";
    	let t0;
    	let t1;
    	let td1;
    	let t2_value = /*student*/ ctx[10].first_name + "";
    	let t2;
    	let t3;
    	let td2;
    	let t4_value = /*student*/ ctx[10].last_name + "";
    	let t4;
    	let t5;
    	let td3;
    	let t6_value = /*student*/ ctx[10].age + "";
    	let t6;
    	let t7;
    	let td4;
    	let t8_value = /*student*/ ctx[10].grade + "";
    	let t8;
    	let t9;
    	let mounted;
    	let dispose;

    	function click_handler() {
    		return /*click_handler*/ ctx[5](/*student*/ ctx[10]);
    	}

    	const block = {
    		key: key_1,
    		first: null,
    		c: function create() {
    			tr = element("tr");
    			td0 = element("td");
    			t0 = text(t0_value);
    			t1 = space();
    			td1 = element("td");
    			t2 = text(t2_value);
    			t3 = space();
    			td2 = element("td");
    			t4 = text(t4_value);
    			t5 = space();
    			td3 = element("td");
    			t6 = text(t6_value);
    			t7 = space();
    			td4 = element("td");
    			t8 = text(t8_value);
    			t9 = space();
    			add_location(td0, file$1, 68, 8, 1559);
    			add_location(td1, file$1, 69, 8, 1589);
    			add_location(td2, file$1, 70, 8, 1627);
    			add_location(td3, file$1, 71, 8, 1664);
    			add_location(td4, file$1, 72, 8, 1695);
    			add_location(tr, file$1, 67, 6, 1506);
    			this.first = tr;
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, tr, anchor);
    			append_dev(tr, td0);
    			append_dev(td0, t0);
    			append_dev(tr, t1);
    			append_dev(tr, td1);
    			append_dev(td1, t2);
    			append_dev(tr, t3);
    			append_dev(tr, td2);
    			append_dev(td2, t4);
    			append_dev(tr, t5);
    			append_dev(tr, td3);
    			append_dev(td3, t6);
    			append_dev(tr, t7);
    			append_dev(tr, td4);
    			append_dev(td4, t8);
    			append_dev(tr, t9);

    			if (!mounted) {
    				dispose = listen_dev(tr, "click", click_handler, false, false, false, false);
    				mounted = true;
    			}
    		},
    		p: function update(new_ctx, dirty) {
    			ctx = new_ctx;
    			if (dirty & /*students*/ 1 && t0_value !== (t0_value = /*student*/ ctx[10].id + "")) set_data_dev(t0, t0_value);
    			if (dirty & /*students*/ 1 && t2_value !== (t2_value = /*student*/ ctx[10].first_name + "")) set_data_dev(t2, t2_value);
    			if (dirty & /*students*/ 1 && t4_value !== (t4_value = /*student*/ ctx[10].last_name + "")) set_data_dev(t4, t4_value);
    			if (dirty & /*students*/ 1 && t6_value !== (t6_value = /*student*/ ctx[10].age + "")) set_data_dev(t6, t6_value);
    			if (dirty & /*students*/ 1 && t8_value !== (t8_value = /*student*/ ctx[10].grade + "")) set_data_dev(t8, t8_value);
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(tr);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block$1.name,
    		type: "each",
    		source: "(67:4) {#each students as student (student.id)}",
    		ctx
    	});

    	return block;
    }

    // (79:0) {#if selectedStudent}
    function create_if_block$1(ctx) {
    	let div;
    	let input0;
    	let t0;
    	let input1;
    	let t1;
    	let input2;
    	let t2;
    	let input3;
    	let t3;
    	let button0;
    	let t5;
    	let button1;
    	let mounted;
    	let dispose;

    	const block = {
    		c: function create() {
    			div = element("div");
    			input0 = element("input");
    			t0 = space();
    			input1 = element("input");
    			t1 = space();
    			input2 = element("input");
    			t2 = space();
    			input3 = element("input");
    			t3 = space();
    			button0 = element("button");
    			button0.textContent = "Save";
    			t5 = space();
    			button1 = element("button");
    			button1.textContent = "Delete";
    			attr_dev(input0, "placeholder", "First Name");
    			add_location(input0, file$1, 80, 4, 1799);
    			attr_dev(input1, "placeholder", "Last Name");
    			add_location(input1, file$1, 81, 4, 1878);
    			attr_dev(input2, "type", "number");
    			attr_dev(input2, "placeholder", "Age");
    			add_location(input2, file$1, 82, 4, 1955);
    			attr_dev(input3, "type", "number");
    			attr_dev(input3, "placeholder", "Grade");
    			add_location(input3, file$1, 83, 4, 2034);
    			add_location(button0, file$1, 84, 4, 2117);
    			add_location(button1, file$1, 85, 4, 2166);
    			add_location(div, file$1, 79, 2, 1789);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);
    			append_dev(div, input0);
    			set_input_value(input0, /*selectedStudent*/ ctx[1].first_name);
    			append_dev(div, t0);
    			append_dev(div, input1);
    			set_input_value(input1, /*selectedStudent*/ ctx[1].last_name);
    			append_dev(div, t1);
    			append_dev(div, input2);
    			set_input_value(input2, /*selectedStudent*/ ctx[1].age);
    			append_dev(div, t2);
    			append_dev(div, input3);
    			set_input_value(input3, /*selectedStudent*/ ctx[1].grade);
    			append_dev(div, t3);
    			append_dev(div, button0);
    			append_dev(div, t5);
    			append_dev(div, button1);

    			if (!mounted) {
    				dispose = [
    					listen_dev(input0, "input", /*input0_input_handler*/ ctx[6]),
    					listen_dev(input1, "input", /*input1_input_handler*/ ctx[7]),
    					listen_dev(input2, "input", /*input2_input_handler*/ ctx[8]),
    					listen_dev(input3, "input", /*input3_input_handler*/ ctx[9]),
    					listen_dev(button0, "click", /*saveStudent*/ ctx[3], false, false, false, false),
    					listen_dev(button1, "click", /*deleteStudent*/ ctx[4], false, false, false, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(ctx, dirty) {
    			if (dirty & /*selectedStudent*/ 2 && input0.value !== /*selectedStudent*/ ctx[1].first_name) {
    				set_input_value(input0, /*selectedStudent*/ ctx[1].first_name);
    			}

    			if (dirty & /*selectedStudent*/ 2 && input1.value !== /*selectedStudent*/ ctx[1].last_name) {
    				set_input_value(input1, /*selectedStudent*/ ctx[1].last_name);
    			}

    			if (dirty & /*selectedStudent*/ 2 && to_number(input2.value) !== /*selectedStudent*/ ctx[1].age) {
    				set_input_value(input2, /*selectedStudent*/ ctx[1].age);
    			}

    			if (dirty & /*selectedStudent*/ 2 && to_number(input3.value) !== /*selectedStudent*/ ctx[1].grade) {
    				set_input_value(input3, /*selectedStudent*/ ctx[1].grade);
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_if_block$1.name,
    		type: "if",
    		source: "(79:0) {#if selectedStudent}",
    		ctx
    	});

    	return block;
    }

    function create_fragment$1(ctx) {
    	let table;
    	let thead;
    	let tr;
    	let th0;
    	let t1;
    	let th1;
    	let t3;
    	let th2;
    	let t5;
    	let th3;
    	let t7;
    	let th4;
    	let t9;
    	let tbody;
    	let each_blocks = [];
    	let each_1_lookup = new Map();
    	let t10;
    	let if_block_anchor;
    	let each_value = /*students*/ ctx[0];
    	validate_each_argument(each_value);
    	const get_key = ctx => /*student*/ ctx[10].id;
    	validate_each_keys(ctx, each_value, get_each_context$1, get_key);

    	for (let i = 0; i < each_value.length; i += 1) {
    		let child_ctx = get_each_context$1(ctx, each_value, i);
    		let key = get_key(child_ctx);
    		each_1_lookup.set(key, each_blocks[i] = create_each_block$1(key, child_ctx));
    	}

    	let if_block = /*selectedStudent*/ ctx[1] && create_if_block$1(ctx);

    	const block = {
    		c: function create() {
    			table = element("table");
    			thead = element("thead");
    			tr = element("tr");
    			th0 = element("th");
    			th0.textContent = "ID";
    			t1 = space();
    			th1 = element("th");
    			th1.textContent = "First Name";
    			t3 = space();
    			th2 = element("th");
    			th2.textContent = "Last Name";
    			t5 = space();
    			th3 = element("th");
    			th3.textContent = "Age";
    			t7 = space();
    			th4 = element("th");
    			th4.textContent = "Grade";
    			t9 = space();
    			tbody = element("tbody");

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].c();
    			}

    			t10 = space();
    			if (if_block) if_block.c();
    			if_block_anchor = empty();
    			add_location(th0, file$1, 58, 6, 1321);
    			add_location(th1, file$1, 59, 6, 1339);
    			add_location(th2, file$1, 60, 6, 1365);
    			add_location(th3, file$1, 61, 6, 1390);
    			add_location(th4, file$1, 62, 6, 1409);
    			add_location(tr, file$1, 57, 4, 1310);
    			add_location(thead, file$1, 56, 2, 1298);
    			add_location(tbody, file$1, 65, 2, 1447);
    			add_location(table, file$1, 55, 0, 1288);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, table, anchor);
    			append_dev(table, thead);
    			append_dev(thead, tr);
    			append_dev(tr, th0);
    			append_dev(tr, t1);
    			append_dev(tr, th1);
    			append_dev(tr, t3);
    			append_dev(tr, th2);
    			append_dev(tr, t5);
    			append_dev(tr, th3);
    			append_dev(tr, t7);
    			append_dev(tr, th4);
    			append_dev(table, t9);
    			append_dev(table, tbody);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				if (each_blocks[i]) {
    					each_blocks[i].m(tbody, null);
    				}
    			}

    			insert_dev(target, t10, anchor);
    			if (if_block) if_block.m(target, anchor);
    			insert_dev(target, if_block_anchor, anchor);
    		},
    		p: function update(ctx, [dirty]) {
    			if (dirty & /*selectStudent, students*/ 5) {
    				each_value = /*students*/ ctx[0];
    				validate_each_argument(each_value);
    				validate_each_keys(ctx, each_value, get_each_context$1, get_key);
    				each_blocks = update_keyed_each(each_blocks, dirty, get_key, 1, ctx, each_value, each_1_lookup, tbody, destroy_block, create_each_block$1, null, get_each_context$1);
    			}

    			if (/*selectedStudent*/ ctx[1]) {
    				if (if_block) {
    					if_block.p(ctx, dirty);
    				} else {
    					if_block = create_if_block$1(ctx);
    					if_block.c();
    					if_block.m(if_block_anchor.parentNode, if_block_anchor);
    				}
    			} else if (if_block) {
    				if_block.d(1);
    				if_block = null;
    			}
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(table);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].d();
    			}

    			if (detaching) detach_dev(t10);
    			if (if_block) if_block.d(detaching);
    			if (detaching) detach_dev(if_block_anchor);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$1.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$1($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Table', slots, []);
    	let students = [];
    	let selectedStudent = null;

    	onMount(async () => {
    		const res = await fetch('http://localhost:8000/api/execute/', {
    			method: 'POST',
    			headers: { 'Content-Type': 'application/json' },
    			body: JSON.stringify({ action: 'fetch_all' })
    		});

    		$$invalidate(0, students = await res.json());
    	});

    	function selectStudent(student) {
    		$$invalidate(1, selectedStudent = student);
    	}

    	async function saveStudent() {
    		// Add or update a student
    		const action = selectedStudent.id ? 'update' : 'insert';

    		const res = await fetch('http://localhost:8000/api/execute', {
    			method: 'POST',
    			headers: { 'Content-Type': 'application/json' },
    			body: JSON.stringify({
    				action,
    				data: { student: selectedStudent }
    			})
    		});

    		$$invalidate(0, students = await res.json());
    	}

    	async function deleteStudent() {
    		// Delete a student
    		const res = await fetch('http://localhost:8000/api/execute', {
    			method: 'POST',
    			headers: { 'Content-Type': 'application/json' },
    			body: JSON.stringify({
    				action: 'delete',
    				data: { id: selectedStudent.id }
    			})
    		});

    		$$invalidate(0, students = await res.json());
    	}

    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Table> was created with unknown prop '${key}'`);
    	});

    	const click_handler = student => selectStudent(student);

    	function input0_input_handler() {
    		selectedStudent.first_name = this.value;
    		$$invalidate(1, selectedStudent);
    	}

    	function input1_input_handler() {
    		selectedStudent.last_name = this.value;
    		$$invalidate(1, selectedStudent);
    	}

    	function input2_input_handler() {
    		selectedStudent.age = to_number(this.value);
    		$$invalidate(1, selectedStudent);
    	}

    	function input3_input_handler() {
    		selectedStudent.grade = to_number(this.value);
    		$$invalidate(1, selectedStudent);
    	}

    	$$self.$capture_state = () => ({
    		onMount,
    		students,
    		selectedStudent,
    		selectStudent,
    		saveStudent,
    		deleteStudent
    	});

    	$$self.$inject_state = $$props => {
    		if ('students' in $$props) $$invalidate(0, students = $$props.students);
    		if ('selectedStudent' in $$props) $$invalidate(1, selectedStudent = $$props.selectedStudent);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [
    		students,
    		selectedStudent,
    		selectStudent,
    		saveStudent,
    		deleteStudent,
    		click_handler,
    		input0_input_handler,
    		input1_input_handler,
    		input2_input_handler,
    		input3_input_handler
    	];
    }

    class Table extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$1, create_fragment$1, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Table",
    			options,
    			id: create_fragment$1.name
    		});
    	}
    }

    /* src/App.svelte generated by Svelte v3.59.2 */

    const { console: console_1 } = globals;
    const file = "src/App.svelte";

    function get_each_context(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[11] = list[i];
    	child_ctx[12] = list;
    	child_ctx[13] = i;
    	return child_ctx;
    }

    function get_each_context_1(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[14] = list[i];
    	return child_ctx;
    }

    function get_each_context_2(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[17] = list[i];
    	child_ctx[18] = list;
    	child_ctx[19] = i;
    	return child_ctx;
    }

    function get_each_context_3(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[11] = list[i];
    	return child_ctx;
    }

    // (35:0) {:else}
    function create_else_block(ctx) {
    	let h1;
    	let t0;
    	let t1;

    	const block = {
    		c: function create() {
    			h1 = element("h1");
    			t0 = text("csrfToken: ");
    			t1 = text(/*csrfToken*/ ctx[0]);
    			add_location(h1, file, 35, 2, 1360);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, h1, anchor);
    			append_dev(h1, t0);
    			append_dev(h1, t1);
    		},
    		p: function update(ctx, dirty) {
    			if (dirty & /*csrfToken*/ 1) set_data_dev(t1, /*csrfToken*/ ctx[0]);
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(h1);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_else_block.name,
    		type: "else",
    		source: "(35:0) {:else}",
    		ctx
    	});

    	return block;
    }

    // (33:0) {#if csrfToken == "fetching csrfToken..."}
    function create_if_block(ctx) {
    	let h1;

    	const block = {
    		c: function create() {
    			h1 = element("h1");
    			h1.textContent = "Fetching csrfToken...";
    			add_location(h1, file, 33, 2, 1319);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, h1, anchor);
    		},
    		p: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(h1);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_if_block.name,
    		type: "if",
    		source: "(33:0) {#if csrfToken == \\\"fetching csrfToken...\\\"}",
    		ctx
    	});

    	return block;
    }

    // (40:2) {#each columns as column}
    function create_each_block_3(ctx) {
    	let th;
    	let t_value = /*column*/ ctx[11] + "";
    	let t;

    	const block = {
    		c: function create() {
    			th = element("th");
    			t = text(t_value);
    			add_location(th, file, 40, 3, 1443);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, th, anchor);
    			append_dev(th, t);
    		},
    		p: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(th);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block_3.name,
    		type: "each",
    		source: "(40:2) {#each columns as column}",
    		ctx
    	});

    	return block;
    }

    // (47:3) {#each row as cell}
    function create_each_block_2(ctx) {
    	let td;
    	let mounted;
    	let dispose;

    	function td_input_handler() {
    		/*td_input_handler*/ ctx[7].call(td, /*each_value_2*/ ctx[18], /*cell_index*/ ctx[19]);
    	}

    	const block = {
    		c: function create() {
    			td = element("td");
    			attr_dev(td, "contenteditable", "true");
    			attr_dev(td, "class", "svelte-o0qdmk");
    			if (/*cell*/ ctx[17] === void 0) add_render_callback(td_input_handler);
    			add_location(td, file, 47, 8, 1539);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, td, anchor);

    			if (/*cell*/ ctx[17] !== void 0) {
    				td.innerHTML = /*cell*/ ctx[17];
    			}

    			if (!mounted) {
    				dispose = listen_dev(td, "input", td_input_handler);
    				mounted = true;
    			}
    		},
    		p: function update(new_ctx, dirty) {
    			ctx = new_ctx;

    			if (dirty & /*data*/ 2 && /*cell*/ ctx[17] !== td.innerHTML) {
    				td.innerHTML = /*cell*/ ctx[17];
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(td);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block_2.name,
    		type: "each",
    		source: "(47:3) {#each row as cell}",
    		ctx
    	});

    	return block;
    }

    // (45:1) {#each data as row}
    function create_each_block_1(ctx) {
    	let tr;
    	let t0;
    	let button0;
    	let t2;
    	let button1;
    	let mounted;
    	let dispose;
    	let each_value_2 = /*row*/ ctx[14];
    	validate_each_argument(each_value_2);
    	let each_blocks = [];

    	for (let i = 0; i < each_value_2.length; i += 1) {
    		each_blocks[i] = create_each_block_2(get_each_context_2(ctx, each_value_2, i));
    	}

    	function click_handler() {
    		return /*click_handler*/ ctx[8](/*row*/ ctx[14]);
    	}

    	function click_handler_1() {
    		return /*click_handler_1*/ ctx[9](/*row*/ ctx[14]);
    	}

    	const block = {
    		c: function create() {
    			tr = element("tr");

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].c();
    			}

    			t0 = space();
    			button0 = element("button");
    			button0.textContent = "X";
    			t2 = space();
    			button1 = element("button");
    			button1.textContent = "save changes";
    			add_location(button0, file, 49, 3, 1605);
    			add_location(button1, file, 50, 6, 1662);
    			attr_dev(tr, "class", "svelte-o0qdmk");
    			add_location(tr, file, 45, 2, 1503);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, tr, anchor);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				if (each_blocks[i]) {
    					each_blocks[i].m(tr, null);
    				}
    			}

    			append_dev(tr, t0);
    			append_dev(tr, button0);
    			append_dev(tr, t2);
    			append_dev(tr, button1);

    			if (!mounted) {
    				dispose = [
    					listen_dev(button0, "click", click_handler, false, false, false, false),
    					listen_dev(button1, "click", click_handler_1, false, false, false, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(new_ctx, dirty) {
    			ctx = new_ctx;

    			if (dirty & /*data*/ 2) {
    				each_value_2 = /*row*/ ctx[14];
    				validate_each_argument(each_value_2);
    				let i;

    				for (i = 0; i < each_value_2.length; i += 1) {
    					const child_ctx = get_each_context_2(ctx, each_value_2, i);

    					if (each_blocks[i]) {
    						each_blocks[i].p(child_ctx, dirty);
    					} else {
    						each_blocks[i] = create_each_block_2(child_ctx);
    						each_blocks[i].c();
    						each_blocks[i].m(tr, t0);
    					}
    				}

    				for (; i < each_blocks.length; i += 1) {
    					each_blocks[i].d(1);
    				}

    				each_blocks.length = each_value_2.length;
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(tr);
    			destroy_each(each_blocks, detaching);
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block_1.name,
    		type: "each",
    		source: "(45:1) {#each data as row}",
    		ctx
    	});

    	return block;
    }

    // (56:2) {#each newRow as column}
    function create_each_block(ctx) {
    	let td;
    	let mounted;
    	let dispose;

    	function td_input_handler_1() {
    		/*td_input_handler_1*/ ctx[10].call(td, /*each_value*/ ctx[12], /*column_index*/ ctx[13]);
    	}

    	const block = {
    		c: function create() {
    			td = element("td");
    			attr_dev(td, "contenteditable", "true");
    			attr_dev(td, "class", "svelte-o0qdmk");
    			if (/*column*/ ctx[11] === void 0) add_render_callback(td_input_handler_1);
    			add_location(td, file, 56, 3, 1795);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, td, anchor);

    			if (/*column*/ ctx[11] !== void 0) {
    				td.innerHTML = /*column*/ ctx[11];
    			}

    			if (!mounted) {
    				dispose = listen_dev(td, "input", td_input_handler_1);
    				mounted = true;
    			}
    		},
    		p: function update(new_ctx, dirty) {
    			ctx = new_ctx;

    			if (dirty & /*newRow*/ 4 && /*column*/ ctx[11] !== td.innerHTML) {
    				td.innerHTML = /*column*/ ctx[11];
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(td);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block.name,
    		type: "each",
    		source: "(56:2) {#each newRow as column}",
    		ctx
    	});

    	return block;
    }

    function create_fragment(ctx) {
    	let t0;
    	let table;
    	let tr0;
    	let t1;
    	let t2;
    	let tr1;
    	let t3;
    	let button;
    	let t5;
    	let pre;
    	let t6_value = JSON.stringify(/*data*/ ctx[1], null, 2) + "";
    	let t6;
    	let mounted;
    	let dispose;

    	function select_block_type(ctx, dirty) {
    		if (/*csrfToken*/ ctx[0] == "fetching csrfToken...") return create_if_block;
    		return create_else_block;
    	}

    	let current_block_type = select_block_type(ctx);
    	let if_block = current_block_type(ctx);
    	let each_value_3 = /*columns*/ ctx[6];
    	validate_each_argument(each_value_3);
    	let each_blocks_2 = [];

    	for (let i = 0; i < each_value_3.length; i += 1) {
    		each_blocks_2[i] = create_each_block_3(get_each_context_3(ctx, each_value_3, i));
    	}

    	let each_value_1 = /*data*/ ctx[1];
    	validate_each_argument(each_value_1);
    	let each_blocks_1 = [];

    	for (let i = 0; i < each_value_1.length; i += 1) {
    		each_blocks_1[i] = create_each_block_1(get_each_context_1(ctx, each_value_1, i));
    	}

    	let each_value = /*newRow*/ ctx[2];
    	validate_each_argument(each_value);
    	let each_blocks = [];

    	for (let i = 0; i < each_value.length; i += 1) {
    		each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
    	}

    	const block = {
    		c: function create() {
    			if_block.c();
    			t0 = space();
    			table = element("table");
    			tr0 = element("tr");

    			for (let i = 0; i < each_blocks_2.length; i += 1) {
    				each_blocks_2[i].c();
    			}

    			t1 = space();

    			for (let i = 0; i < each_blocks_1.length; i += 1) {
    				each_blocks_1[i].c();
    			}

    			t2 = space();
    			tr1 = element("tr");

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].c();
    			}

    			t3 = space();
    			button = element("button");
    			button.textContent = "add";
    			t5 = space();
    			pre = element("pre");
    			t6 = text(t6_value);
    			add_location(tr0, file, 38, 1, 1407);
    			add_location(button, file, 58, 2, 1861);
    			set_style(tr1, "color", "grey");
    			attr_dev(tr1, "class", "svelte-o0qdmk");
    			add_location(tr1, file, 54, 1, 1740);
    			set_style(pre, "background", "#eee");
    			add_location(pre, file, 62, 1, 1910);
    			add_location(table, file, 37, 0, 1398);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			if_block.m(target, anchor);
    			insert_dev(target, t0, anchor);
    			insert_dev(target, table, anchor);
    			append_dev(table, tr0);

    			for (let i = 0; i < each_blocks_2.length; i += 1) {
    				if (each_blocks_2[i]) {
    					each_blocks_2[i].m(tr0, null);
    				}
    			}

    			append_dev(table, t1);

    			for (let i = 0; i < each_blocks_1.length; i += 1) {
    				if (each_blocks_1[i]) {
    					each_blocks_1[i].m(table, null);
    				}
    			}

    			append_dev(table, t2);
    			append_dev(table, tr1);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				if (each_blocks[i]) {
    					each_blocks[i].m(tr1, null);
    				}
    			}

    			append_dev(tr1, t3);
    			append_dev(tr1, button);
    			append_dev(table, t5);
    			append_dev(table, pre);
    			append_dev(pre, t6);

    			if (!mounted) {
    				dispose = listen_dev(button, "click", /*addRow*/ ctx[3], false, false, false, false);
    				mounted = true;
    			}
    		},
    		p: function update(ctx, [dirty]) {
    			if (current_block_type === (current_block_type = select_block_type(ctx)) && if_block) {
    				if_block.p(ctx, dirty);
    			} else {
    				if_block.d(1);
    				if_block = current_block_type(ctx);

    				if (if_block) {
    					if_block.c();
    					if_block.m(t0.parentNode, t0);
    				}
    			}

    			if (dirty & /*columns*/ 64) {
    				each_value_3 = /*columns*/ ctx[6];
    				validate_each_argument(each_value_3);
    				let i;

    				for (i = 0; i < each_value_3.length; i += 1) {
    					const child_ctx = get_each_context_3(ctx, each_value_3, i);

    					if (each_blocks_2[i]) {
    						each_blocks_2[i].p(child_ctx, dirty);
    					} else {
    						each_blocks_2[i] = create_each_block_3(child_ctx);
    						each_blocks_2[i].c();
    						each_blocks_2[i].m(tr0, null);
    					}
    				}

    				for (; i < each_blocks_2.length; i += 1) {
    					each_blocks_2[i].d(1);
    				}

    				each_blocks_2.length = each_value_3.length;
    			}

    			if (dirty & /*update, data, deleteRow*/ 50) {
    				each_value_1 = /*data*/ ctx[1];
    				validate_each_argument(each_value_1);
    				let i;

    				for (i = 0; i < each_value_1.length; i += 1) {
    					const child_ctx = get_each_context_1(ctx, each_value_1, i);

    					if (each_blocks_1[i]) {
    						each_blocks_1[i].p(child_ctx, dirty);
    					} else {
    						each_blocks_1[i] = create_each_block_1(child_ctx);
    						each_blocks_1[i].c();
    						each_blocks_1[i].m(table, t2);
    					}
    				}

    				for (; i < each_blocks_1.length; i += 1) {
    					each_blocks_1[i].d(1);
    				}

    				each_blocks_1.length = each_value_1.length;
    			}

    			if (dirty & /*newRow*/ 4) {
    				each_value = /*newRow*/ ctx[2];
    				validate_each_argument(each_value);
    				let i;

    				for (i = 0; i < each_value.length; i += 1) {
    					const child_ctx = get_each_context(ctx, each_value, i);

    					if (each_blocks[i]) {
    						each_blocks[i].p(child_ctx, dirty);
    					} else {
    						each_blocks[i] = create_each_block(child_ctx);
    						each_blocks[i].c();
    						each_blocks[i].m(tr1, t3);
    					}
    				}

    				for (; i < each_blocks.length; i += 1) {
    					each_blocks[i].d(1);
    				}

    				each_blocks.length = each_value.length;
    			}

    			if (dirty & /*data*/ 2 && t6_value !== (t6_value = JSON.stringify(/*data*/ ctx[1], null, 2) + "")) set_data_dev(t6, t6_value);
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if_block.d(detaching);
    			if (detaching) detach_dev(t0);
    			if (detaching) detach_dev(table);
    			destroy_each(each_blocks_2, detaching);
    			destroy_each(each_blocks_1, detaching);
    			destroy_each(each_blocks, detaching);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('App', slots, []);

    	function addRow() {
    		$$invalidate(1, data = [...data, [...newRow]]);
    		$$invalidate(2, newRow = ['', "", "", "", '', '', ""]);
    	}

    	function deleteRow(rowToBeDeleted) {
    		$$invalidate(1, data = data.filter(row => row != rowToBeDeleted));
    	}

    	function update(rowToBeEdited) {
    		console.log(data);
    	}

    	let columns = ["ID", "First Name", "Last Name", "Role", "Age", "Grade", "Address"]; // i dea: make this a prop sent from the backend
    	let csrfToken = "fetching csrfToken...";

    	onMount(async () => {
    		fetch('http://localhost:8000/api/csrf/', { method: 'GET' }).then(res => res.json()).then(res => {
    			$$invalidate(0, csrfToken = res.csrfToken);

    			apiActionRequest(csrfToken, 'fetch_all', ["", "", "", "student", "", "", ""]).then(res => {
    				$$invalidate(1, data = res);
    				console.log(res);
    			});
    		});
    	});

    	let data = [
    		['1', "John", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    		['2', "Sarah", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    		['3', "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"]
    	];

    	let newRow = ['', "", "", "", '', '', ""];
    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1.warn(`<App> was created with unknown prop '${key}'`);
    	});

    	function td_input_handler(each_value_2, cell_index) {
    		each_value_2[cell_index] = this.innerHTML;
    		$$invalidate(1, data);
    	}

    	const click_handler = row => deleteRow(row);
    	const click_handler_1 = row => update();

    	function td_input_handler_1(each_value, column_index) {
    		each_value[column_index] = this.innerHTML;
    		$$invalidate(2, newRow);
    	}

    	$$self.$capture_state = () => ({
    		Table,
    		onMount,
    		apiActionRequest,
    		addRow,
    		deleteRow,
    		update,
    		columns,
    		csrfToken,
    		data,
    		newRow
    	});

    	$$self.$inject_state = $$props => {
    		if ('columns' in $$props) $$invalidate(6, columns = $$props.columns);
    		if ('csrfToken' in $$props) $$invalidate(0, csrfToken = $$props.csrfToken);
    		if ('data' in $$props) $$invalidate(1, data = $$props.data);
    		if ('newRow' in $$props) $$invalidate(2, newRow = $$props.newRow);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [
    		csrfToken,
    		data,
    		newRow,
    		addRow,
    		deleteRow,
    		update,
    		columns,
    		td_input_handler,
    		click_handler,
    		click_handler_1,
    		td_input_handler_1
    	];
    }

    class App extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance, create_fragment, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "App",
    			options,
    			id: create_fragment.name
    		});
    	}
    }

    const apiActionRequest = async function (csrfToken, action, data) {
        const request = {
            action: action,
            jwt: "jwt",
            data: {
                id: parseInt(data[0]),
                reference: {
                    first_name: data[1],
                    last_name: data[2],
                    role: data[3],
                    age: data[4],
                    grade: data[5],
                    address: data[6],
                },
            }
        };
        const res = await fetch("http://localhost:8000/api/execute/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(request),
        });
        const rows = [];
        const resJson = await res.json();
        if (resJson.status !== 200) { // If api returns error
            console.log("Error: " + resJson.message);
            return rows;
        }
        else {
            for (let i = 0; i < resJson.data.length; i++) {
                const refData = resJson.data[i];
                const row = [refData.id.toString(), refData.reference.first_name, refData.reference.last_name, refData.reference.role, refData.reference.age, refData.reference.grade, refData.reference.address];
                rows.push(row);
            }
            return rows;
        }
    };
    const app = new App({
        target: document.body,
        props: {},
    });

    exports.apiActionRequest = apiActionRequest;
    exports.default = app;

    Object.defineProperty(exports, '__esModule', { value: true });

    return exports;

})({});
//# sourceMappingURL=bundle.js.map
