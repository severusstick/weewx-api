<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateWeatherPerMinuteTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('weather_per_minutes', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->bigInteger('dateTime')->unique();
            $table->double('heatindex')->nullable();
            $table->double('maxSolarRad')->nullable();
            $table->double('consBatteryVoltage')->nullable();
            $table->double('barometer')->nullable();
            $table->double('outTemp')->nullable();
            $table->double('outHumidity')->nullable();
            $table->double('windSpeed')->nullable();
            $table->double('windDir')->nullable();
            $table->double('windGust')->nullable();
            $table->double('windGustDir')->nullable();
            $table->double('windchill')->nullable();
            $table->double('dewpoint')->nullable();
            $table->double('UV')->nullable();
            $table->double('radiation')->nullable();
            $table->double('hourRain')->nullable();
            $table->double('dayRain')->nullable();
            $table->double('stormRain')->nullable();
            $table->double('cloudbase')->nullable();
            $table->double('sunrise')->nullable();
            $table->double('sunset')->nullable();
            $table->double('forecastIcon')->nullable();
            $table->double('forecastRule')->nullable();
            $table->double('trendIcon')->nullable();
            $table->double('outsideAlarm1')->nullable();
            $table->double('outsideAlarm2')->nullable();
            $table->double('rainAlarm')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('weather_per_minutes');
    }
}
