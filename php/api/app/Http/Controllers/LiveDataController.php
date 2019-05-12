<?php

namespace App\Http\Controllers;

use App\LiveData;
use Illuminate\Http\Request;

class LiveDataController extends Controller
{
	public function updateLiveData(Request $request)
	{
		$live_weather = LiveData::updateOrCreate(['id' => 1], $request->all());

		return response()->json($live_weather, 200);
	}
}
