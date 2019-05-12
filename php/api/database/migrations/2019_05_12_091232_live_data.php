<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class LiveData extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('live_data', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->bigInteger('dateTime')->nullable();
            $table->double('hourRain')->nullable();
            $table->double('dayRain')->nullable();
            $table->double('altimeter')->nullable();
            $table->double('appTemp')->nullable();
            $table->double('barometer')->nullable();
            $table->double('cloudbase')->nullable();
            $table->double('consBatteryVoltage')->nullable();
            $table->double('dewpoint')->nullable();
            $table->double('heatindex')->nullable();
            $table->double('heatingVoltage')->nullable();
            $table->double('humidex')->nullable();
            $table->double('inDewpoint')->nullable();
            $table->double('inHumidity')->nullable();
            $table->double('inTemp')->nullable();
            $table->double('inTempBatteryStatus')->nullable();
            $table->double('maxSolarRad')->nullable();
            $table->double('outHumidity')->nullable();
            $table->double('outTemp')->nullable();
            $table->double('outTempBatteryStatus')->nullable();
            $table->double('radiation')->nullable();
            $table->double('rain')->nullable();
            $table->double('rainBatteryStatus')->nullable();
            $table->double('rainRate')->nullable();
            $table->double('referenceVoltage')->nullable();
            $table->double('rxCheckPercent')->nullable();
            $table->double('supplyVoltage')->nullable();
            $table->double('txBatteryStatus')->nullable();
            $table->double('UV')->nullable();
            $table->double('windBatteryStatus')->nullable();
            $table->double('windchill')->nullable();
            $table->double('windDir')->nullable();
            $table->double('windGust')->nullable();
            $table->double('windGustDir')->nullable();
            $table->double('windSpeed')->nullable();
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
        Schema::dropIfExists('live_data');
    }
}
