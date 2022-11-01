<template>
    <div class="page-location-grid">
        <h2 class="title is-2 has-text-centered">Location Grid</h2>
        <form @submit.prevent="getLocationData()">
            <div class="columns">
                <div class="column">
                    <div class="field has-addons">
                        <div class="control">
                            <input type="text" class="input" placeholder="Search for user" v-model="nameQuery" />
                        </div>
                        <div class="control">
                            <input type="datetime-local" class="input" v-model="fromDateQuery" />
                        </div>
                        <div class="control">
                            <input type="datetime-local" class="input" v-model="toDateQuery" />
                        </div>
                        <div class="control">
                            <button class="button is-success">
                                <span class="icon">
                                    <i class="fa fa-search"></i>
                                </span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
        </form>
        

        <h4 v-if="lastFilter.length" class="subtitle is-4 has-text-centered mt-4">Searching for "{{lastFilter}}"</h4>
        <table class="table mt-5">
            <thead>
                <tr>
                    <th><abbr title="Position">Id</abbr></th>
                    <th><abbr title="User">User</abbr></th>
                    <th><abbr title="Created Date">Created Date</abbr></th>
                    <th><abbr title="City">City</abbr></th>
                    <th><abbr title="Country">Country</abbr></th>
                    <th><abbr title="Latitude">Latitude</abbr></th>
                    <th><abbr title="Longitude">Longitude</abbr></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="location in locationData" :key="location.id">
                <th>{{ location.id }}</th>
                <td>{{ location.email }}</td>
                <td>{{ location.location_date }}</td>
                <td>{{ location.city_name }}</td>
                <td>{{ location.country_name }}</td>
                <td>{{ location.lat }}</td>
                <td>{{ location.lng }}</td>
                </tr>
            </tbody>
            </table>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'LocationGrid',
    data() {
        return {
            locationData: [],
            nameQuery: '',
            fromDateQuery: '',
            toDateQuery: '',
            lastFilter: '',
        }
    },
    created() {
        document.title = "Location Grid" + this.$baseTitle;

        this.getLocationData();
    },
    methods: {
        getLocationData: function() {
            let dateQuery = '';
            if (this.fromDateQuery.length && this.toDateQuery.length) {
                dateQuery = ` '${this.fromDateQuery}' - '${this.toDateQuery}'`
            }

            this.lastFilter = this.nameQuery + dateQuery;

            let params = new URLSearchParams([
                ['email', this.nameQuery]
            ]);

            // Add from/to dates, if given
            if (this.fromDateQuery.length) {
                params.append('from_date', this.fromDateQuery);
            }
            if (this.toDateQuery.length) {
                params.append('to_date', this.toDateQuery);
            }

            axios.get('/api/v1/location/', { params }).then((resp) => {
                if (resp.data) {
                    this.locationData = resp.data;
                }
            }).catch((error) => {
                toast({
                    message: "Error fetching location data.",
                    type: "is-danger",
                    duration: 2000,
                    position: "bottom-right",
                    dismissible: true,
                    pauseOnHover: true
                });

                console.log(error);
            }).then(() => {
                this.nameQuery = '';
                this.fromDateQuery = '';
                this.toDateQuery = '';
            });
        },
    }
}
</script>