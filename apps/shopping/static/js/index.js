"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Define the load_data_url variable
const load_data_url = "/load_data";

app.data = {
    data: function() {
        return {
            newItem: '',
            items: []
        };
    },
    methods: {
        async loadData() {
            try {
                const response = await axios.get(load_data_url);
                this.items = response.data;
            } catch (error) {
                console.error('Error loading data:', error);
            }
        },
        async addItem() {
            if (this.newItem.trim() !== '') {
                try {
                    const response = await axios.post(load_data_url, { name: this.newItem.trim(), purchased: false });
                    this.items.unshift(response.data);
                    this.newItem = '';
                } catch (error) {
                    console.error('Error adding item:', error);
                }
            }
        },
        async togglePurchased(item) {
            try {
                await axios.put(load_data_url + '/' + item.id, { purchased: item.purchased });
                this.sortItems();
            } catch (error) {
                console.error('Error toggling purchased status:', error);
            }
        },
        async deleteItem(index) {
            const item = this.items[index];
            if (confirm('Are you sure you want to delete this item?')) {
                try {
                    await axios.delete(load_data_url + '/' + item.id);
                    this.items.splice(index, 1);
                } catch (error) {
                    console.error('Error deleting item:', error);
                }
            }
        },
        sortItems() {
            this.items.sort((a, b) => {
                if (a.purchased && !b.purchased) {
                    return 1;
                } else if (!a.purchased && b.purchased) {
                    return -1;
                }
                return 0;
            });
        }
    }
};

app.vue = Vue.createApp(app.data).mount("#app");


// This is the initial data load.
app.vue.loadData();
