// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_mode: false,
        add_post_desc: "",
        rows: [],

    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.add_post = function () {
        axios.post(add_post_url,
            {
                post_desc: app.vue.add_post_desc,
            }).then(function (response) {
            app.vue.rows.push({
                id: response.data.id,
                name: response.data.name,
                post_desc: app.vue.add_post_desc,
            });
        app.enumerate(app.vue.rows);
        app.reset_form();
        app.set_add_status(false);

        });

    };

    app.reset_form = function () {
        app.vue.add_post_desc = "";
    };

    app.set_add_status = function(new_status){
        app.vue.add_mode = new_status;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_post: app.add_post,
        set_add_status: app.set_add_status,
        reset_form: app.reset_form,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(load_posts_url).then(function(response) {
            app.vue.rows = app.enumerate(response.data.rows);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
