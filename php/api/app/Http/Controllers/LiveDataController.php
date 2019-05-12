<?php

namespace App\Http\Controllers;

use App\LiveData;
use Illuminate\Http\Request;

class LiveDataController extends Controller
{
	public function updateLiveData(Request $request)
	{
		$live_weather = LiveData::where('id', 1)->updateOrCreate($request->all());

		return response()->json($live_weather, 200);
	}
}
