<template>
    <div class="page-location-form">
        <div class="columns is-centered mt-6">
            <div class="box is-4 is-offset-4">
                <div class="is-4 is-offset-4">
                <h1 class="title">Location Form</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" class="input" v-model="email" placeholder="Enter a valid email..." />
                        </div>
                    </div>
                    <p v-if="failedSubmission && !email.length">Invalid username</p>

                    <div class="field">
                        <label>City</label>
                        <div class="control">
                            <input type="text" class="input" v-model="location" placeholder="Enter a valid city name..." />
                        </div>
                    </div>
                    <p v-if="failedSubmission && !location.length">Invalid location</p>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'LocationForm',
    data() {
        return {
            email: '',
            location: '',
            failedSubmission: false
        }
    },
    created() {
        document.title = "Location Form" + this.$baseTitle;
    },
    methods: {
        submitForm: function() {
            this.failedSubmission = false;

            // First make sure we have a valid form
            if (!this.validateForm()) {
                this.failedSubmission = true;
                toast({
                    message: "Invalid form data.",
                    type: "is-danger",
                    duration: 2000,
                    position: "bottom-right",
                    dismissible: true,
                    pauseOnHover: true
                });

                return;
            }

            // Then submit form data
            const formData = {
                email: this.email,
                city_name: this.location
            };

            axios.post('/api/v1/location/', formData).then((resp) => {
                toast({
                    message: "Location submitted successfully!",
                    type: "is-success",
                    duration: 2000,
                    position: "bottom-right",
                    dismissible: true,
                    pauseOnHover: true
                });

                this.clearForm();
            }).catch((error) => {
                toast({
                    message: "Error submitting form. Please try again",
                    type: "is-danger",
                    duration: 2000,
                    position: "bottom-right",
                    dismissible: true,
                    pauseOnHover: true
                });

                console.log(error);
            });
        },
        validateForm: function() {
            if (!this.email.length) {
                return false;
            }

            if (!this.location.length) {
                return false;
            }

            return true;
        },
        clearForm: function() {
            this.email = '';
            this.location = '';
        }
    }
}
</script>