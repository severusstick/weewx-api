<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', function () use ($router) {
    return $router->app->version();
});

$router->group(['prefix' => 'api'], function () use ($router) {

    /* ned only get and post at the moment */

    // $router->get('weather_minutely',  ['uses' => 'WeatherMinutelyController@showAll']);
    $router->get('weather_minutely/{id}', ['uses' => 'WeatherMinutelyController@showOne']);
    $router->post('weather_minutely', ['uses' => 'WeatherMinutelyController@create']);
    // $router->delete('weather_minutely/{id}', ['uses' => 'WeatherMinutelyController@delete']);
    // $router->put('weather_minutely/{id}', ['uses' => 'WeatherMinutelyController@update']);
});
